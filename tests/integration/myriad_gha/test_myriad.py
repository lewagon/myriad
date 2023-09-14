
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

    data_path = os.path.join("tests", "data", "myriad_gha")
    source_path = os.path.join(data_path, "source")
    control_path = os.path.join(data_path, "control")
    processed_path = os.path.join(data_path, "processed")

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
        qa_solutions = GhRepo("lewagon-qa/qa-solutions", token=token, verbose=True)
        qa_solutions.delete(dry_run=False)
        qa_solutions.create()

        qa_challenge = GhRepo("lewagon-qa/qa-challenge", token=token, verbose=True)
        qa_challenge.delete(dry_run=False)

        # Act
        solutions = GitRepo(os.path.join(self.source_path, "qa-solutions"), verbose=True)
        solutions.init()
        solutions.add()
        solutions.commit(message="initial commit")
        solutions.remote_add(qa_solutions)
        solutions.push(branch="master")
        solutions.delete_git_dir()

        # the `myriad gha` is being triggered on `lewagon-qa/qa-solutions` as a result of the push
        # wait for `lewagon-qa/qa-challenge` to be created as a result of the `myriad gha`
        qa_challenge.wait_for_creation()

        processed_challenge = GitRepo(os.path.join(self.processed_path, "qa-challenge"), verbose=True)
        processed_challenge.clone(qa_challenge)
        processed_challenge.delete_git_dir()

        # Assert
        control_challenge_path = os.path.join(self.control_path, "qa-challenge")

        rc, output, error = are_directories_identical(
            processed_challenge.path, control_challenge_path)

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
        shutil.rmtree(processed_challenge.path, ignore_errors=True)

        qa_challenge.delete(dry_run=False)

        qa_solutions.delete(dry_run=False)
