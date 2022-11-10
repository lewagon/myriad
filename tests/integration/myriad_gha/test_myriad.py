
from wagon_common.git.git_repo import GitRepo
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

        gha_solutions_path = os.path.join(source_path, "gha-solutions")
        gha_solutions_pr_path = os.path.join(source_path, "gha-solutions-pr")

        gha_challenge_path = os.path.join(control_path, "gha-challenge")
        gha_challenge_pr_path = os.path.join(control_path, "gha-challenge-pr")

        gh_solutions_repo = GHRepo("Le-Wagon-QA/gha-solutions")
        gh_solutions_repo.delete()

        gh_challenge_repo = GHRepo("Le-Wagon-QA/gha-challenge")
        gh_challenge_repo.delete()

        solutions_repo = GitRepo(gha_solutions_path)
        solutions_repo.init()
        solutions_repo.commit(message="initial commit")
        solutions_repo.remote_add("origin", gh_solutions_repo.name)

        # Act
        solutions_repo.push()

        # 🔥 TODO

        # Assert
        control_challenge_repo = GitRepo(gha_challenge_path)

        processed_challenge_repo = GitRepo(gha_challenge_path_TODO)
        processed_challenge_repo.remote_add("origin", gh_challenge_repo.name)
        processed_challenge_repo.wait_for_creation()
        processed_challenge_repo.clone()


        rc, output, error = are_directories_identical(out_path, control_path)

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
        shutil.rmtree(out_path, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
