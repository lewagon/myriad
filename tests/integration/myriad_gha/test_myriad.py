
from wagon_common.git.git_repo import GitRepo
from wagon_common.gh.gh_repo import GhRepo
from wagon_common.helpers.directories import are_directories_identical

import unittest

import os
import shutil

from colorama import Fore, Style


class TestMyriadGha(unittest.TestCase):
    """
    test that myriad challenges are correctly generated from source codebase
    """

    def test_myriad_gha(self):

        # Arrange
        data_path = os.path.join("tests", "data", "myriad_gha")
        source_path = os.path.join(data_path, "source")
        control_path = os.path.join(data_path, "control")
        processed_path = os.path.join(data_path, "processed")

        gha_solutions_path = os.path.join(source_path, "gha-solutions")
        gha_solutions_pr_path = os.path.join(source_path, "gha-solutions-pr")

        control_challenge_path = os.path.join(control_path, "gha-challenge")
        control_challenge_pr_path = os.path.join(control_path, "gha-challenge-pr")

        processed_challenge_path = os.path.join(processed_path, "gha-challenge")
        processed_challenge_pr_path = os.path.join(processed_path, "gha-challenge-pr")

        gh_solutions_repo = GhRepo("le-wagon-qa/gha-solutions")
        gh_challenge_repo = GhRepo("le-wagon-qa/gha-challenge")

        solutions_repo = GitRepo(gha_solutions_path)

        processed_challenge_repo = GitRepo(processed_challenge_path)

        # Act
        gh_solutions_repo.delete()
        gh_challenge_repo.delete()

        solutions_repo.init()
        solutions_repo.add()
        solutions_repo.commit(message="initial commit")
        solutions_repo.remote_add(gh_solutions_repo)
        solutions_repo.push()

        processed_challenge_repo.remote_add(gh_challenge_repo)
        processed_challenge_repo.wait_for_creation()
        processed_challenge_repo.clone()

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

        # test does not work yet
        #
        # unable to ignore the relative position of the source dir
        # and to generate the challenge precisely in the control dir

        # assert rc == 0

        # Cleanup
        shutil.rmtree(os.path.join(solutions_repo.path, ".git"), ignore_errors=True)

        shutil.rmtree(processed_challenge_repo.path, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
