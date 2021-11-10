"""
loads legacy syllabus from cloned meta repo
"""

import os
import yaml

from colorama import Fore, Style

from wagon_myriad.models.syllabus.syllabus import Syllabus

from wagon_myriad.models.syllabus.utils import parse_syllabus


class ClonedSyllabus(Syllabus):

    def __init__(self, path):

        self.path = path

        super().__init__()

    def load_syllabus(self):
        """
        load and parse syllabus yaml file
        """

        # load syllabus
        syllabus_content = self.__load_meta_syllabus(self.path)

        # parse syllabus
        (
            self.modules,
            self.leafs,
            self.challenges,
            self.lectures,
            self.videos) = parse_syllabus(syllabus_content)

    def __load_meta_syllabus(self, meta_repo_path):
        """
        read syllabus yaml file
        """

        # retrieve syllabus content
        syllabus_path = os.path.join(
            meta_repo_path,
            "syllabus.yml")

        # check if file exists
        if not os.path.isfile(syllabus_path):

            print(Fore.RED
                  + f"\nMeta syllabus {syllabus_path} does not exist"
                  + Style.RESET_ALL
                  + "\nCannot continue")

            # return an empty syllabus
            return {}

        # load syllabus
        with open(syllabus_path, "r") as file:
            syllabus = yaml.safe_load(file)

        return syllabus


if __name__ == '__main__':

    for course in ["data", "fullstack"]:

        meta_repo_path = os.path.relpath(os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "..",
            "..",
            f"{course}-meta"))

        cloned_syllabus = ClonedSyllabus(meta_repo_path)

        print(f"loaded {course} challenges: {len(cloned_syllabus.challenges)}")
