
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
        data_path = os.path.join("tests", "data", "run")

        in_path = os.path.join(data_path, "source")
        out_path = os.path.join(data_path, "processed")
        control_path = os.path.join(data_path, "control")

        # Act

        # 🔥 TODO

        # Assert
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
