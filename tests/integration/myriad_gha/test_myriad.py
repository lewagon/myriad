
from wagon_common.git.git_repo import GitRepo
from wagon_common.gh.gh_repo import GhRepo
from wagon_common.helpers.directories import are_directories_identical

import unittest

import os
import shutil

from colorama import Fore, Style

import pytest

from dotenv import load_dotenv, find_dotenv


class TestMyriadGha():
    """
    test that myriad challenges are correctly generated from source codebase
    """

    @pytest.fixture
    def token(self):
        """
        fetch gh token to perform the tests
        """

        # Arrange
        load_dotenv(find_dotenv())
        token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

        # Act & Assert
        yield token

        # Cleanup

    def test_myriad_gha(self, token):

        # Arrange
        data_path = os.path.join("tests", "data", "myriad_gha")
        source_path = os.path.join(data_path, "source")
        control_path = os.path.join(data_path, "control")
        processed_path = os.path.join(data_path, "processed")

        gha_solutions_path = os.path.join(source_path, "qa-solutions")
        control_challenge_path = os.path.join(control_path, "qa-challenge")
        processed_challenge_path = os.path.join(processed_path, "qa-challenge")

        # gha_solutions_pr_path = os.path.join(source_path, "qa-solutions-pr")
        # control_challenge_pr_path = os.path.join(control_path, "qa-challenge-pr")
        # processed_challenge_pr_path = os.path.join(processed_path, "qa-challenge-pr")

        gh_solutions_repo = GhRepo("lewagon-qa/qa-solutions", token=token, verbose=True)
        gh_challenge_repo = GhRepo("lewagon-qa/qa-challenge", token=token, verbose=True)

        solutions_repo = GitRepo(gha_solutions_path, verbose=True)

        processed_challenge_repo = GitRepo(processed_challenge_path, verbose=True)

        # Act
        gh_solutions_repo.delete(dry_run=False)
        gh_challenge_repo.delete(dry_run=False)

        gh_solutions_repo.create()

        solutions_repo.config_user_name()
        solutions_repo.config_user_email()

        solutions_repo.init()
        solutions_repo.add()
        solutions_repo.commit(message="initial commit")
        solutions_repo.set_branch()
        solutions_repo.remote_add(gh_solutions_repo, https=True)
        solutions_repo.set_remote_branch()

        # solutions_repo.checkout()
        # solutions_repo.push(branch="master")
        # solutions_repo.push(branch="master", set_upstream=True)

        gh_challenge_repo.wait_for_creation()

        processed_challenge_repo.clone(gh_challenge_repo)

        # Assert
        shutil.rmtree(os.path.join(processed_challenge_repo.path, ".git"), ignore_errors=True)

        rc, output, error = are_directories_identical(processed_challenge_repo.path, control_challenge_path)

        if rc != 0:

            print(Fore.RED
                  + "\nDirectory content does not match 🤕"
                  + Style.RESET_ALL
                  + f"\n- rc: {rc}"
                  + f"\n- output: {output}"
                  + f"\n- error: {error}")
            print(output.decode("utf-8"))

        assert rc == 0

        # Cleanup
        gh_solutions_repo.delete(dry_run=False)
        gh_challenge_repo.delete(dry_run=False)

        shutil.rmtree(os.path.join(solutions_repo.path, ".git"), ignore_errors=True)

        shutil.rmtree(processed_challenge_repo.path, ignore_errors=True)
