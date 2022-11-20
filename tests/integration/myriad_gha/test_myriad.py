
from wagon_common.git.git_repo import GitRepo
from wagon_common.gh.gh_repo import GhRepo
from wagon_common.helpers.directories import are_directories_identical

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
        token = os.environ["GH_API_DELETE_TOKEN"]

        # Act & Assert
        yield token

        # Cleanup

    def test_myriad_gha(self, token):

        # Arrange
        data_path = os.path.join("tests", "data", "myriad_gha")
        source_path = os.path.join(data_path, "source")
        control_path = os.path.join(data_path, "control")
        processed_path = os.path.join(data_path, "processed")

        solutions_path = os.path.join(source_path, "qa-solutions")
        control_challenge_path = os.path.join(control_path, "qa-challenge")
        processed_challenge_path = os.path.join(processed_path, "qa-challenge")

        # gha_solutions_pr_path = os.path.join(source_path, "qa-solutions-pr")
        # control_challenge_pr_path = os.path.join(control_path, "qa-challenge-pr")
        # processed_challenge_pr_path = os.path.join(processed_path, "qa-challenge-pr")

        qa_solutions = GhRepo("lewagon-qa/qa-solutions", token=token, verbose=True)
        qa_challenge = GhRepo("lewagon-qa/qa-challenge", token=token, verbose=True)

        solutions = GitRepo(solutions_path, verbose=True)

        processed_challenge = GitRepo(processed_challenge_path, verbose=True)

        # Act
        qa_solutions.delete(dry_run=False)
        qa_challenge.delete(dry_run=False)

        qa_solutions.create()

        solutions.init(initial_branch="master")
        solutions.add()
        solutions.commit(message="initial commit")
        solutions.remote_add(qa_solutions, https=True)
        solutions.push(branch="master")

        qa_challenge.wait_for_creation()

        processed_challenge.clone(qa_challenge)

        # Assert
        shutil.rmtree(os.path.join(processed_challenge.path, ".git"), ignore_errors=True)

        rc, output, error = are_directories_identical(processed_challenge.path, control_challenge_path)

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
        qa_solutions.delete(dry_run=False)
        qa_challenge.delete(dry_run=False)

        shutil.rmtree(os.path.join(solutions.path, ".git"), ignore_errors=True)

        shutil.rmtree(processed_challenge.path, ignore_errors=True)
