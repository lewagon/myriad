"""
loads challenge list from repo meta directories
"""

import os
import glob

from colorama import Fore, Style

from wagon_myriad.models.syllabus.syllabus import Syllabus

from wagon_myriad.models.repo.yaml_file import YamlFile
from wagon_myriad.models.challenge.dot_challenge import DotChallenge
from wagon_myriad.params.meta import (
    SOLUTION_META_DIRECTORY, SOLUTION_META_FILE)


class DotSyllabus(Syllabus):

    def __init__(self, path):

        self.path = path

        super().__init__()

    def load_syllabus(self):

        print(Fore.GREEN
              + "\nGet dot syllabus"
              + Style.RESET_ALL
              + f"\n- path: {self.path}")

        # build meta directories pattern
        pattern_suffix = os.path.join(
            SOLUTION_META_DIRECTORY,
            SOLUTION_META_FILE)

        meta_dir_pattern = os.path.join(
            self.path,
            "**",
            pattern_suffix)

        # list meta directories
        meta_directory_files = glob.glob(
            meta_dir_pattern, recursive=True)  # root_dir not yet available

        # iterate through directories
        challenges = []

        for meta_file_path in sorted(meta_directory_files):

            # build challenge path
            prefix_len = len(self.path) + 1
            suffix_len = len(pattern_suffix) + 1

            challenge_path = meta_file_path[prefix_len:-suffix_len]

            # load meta data
            dot_meta_file = YamlFile(meta_file_path)
            metadata = dot_meta_file.load()

            # add challenge
            challenge = DotChallenge(challenge_path, metadata)

            challenges.append(challenge)

        # store challenges
        self.challenges = challenges


if __name__ == '__main__':

    repo_path = os.path.relpath(os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "..",
        "..",
        "data-solutions"))

    data_dot_syllabus = DotSyllabus(repo_path)

    print(f"loaded data challenges: {len(data_dot_syllabus.challenges)}")

    for challenge in data_dot_syllabus.challenges:

        print(challenge)
