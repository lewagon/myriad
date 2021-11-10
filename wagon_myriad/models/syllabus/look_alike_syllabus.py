"""
loads challenge list from look alike directories
"""

import os
import glob

from colorama import Fore, Style

from wagon_myriad.models.syllabus.syllabus import Syllabus

from wagon_myriad.github.context import get_challenge_path

from wagon_myriad.models.challenge.challenge import Challenge


class LookAlikeSyllabus(Syllabus):

    def __init__(self, path, use_readmes=False):

        self.path = path

        self.use_readmes = use_readmes

        super().__init__()

    def load_syllabus(self):

        print(Fore.GREEN
              + "\nGet " + ("look alike" if self.use_readmes else "readme") + " syllabus"
              + Style.RESET_ALL
              + f"\n- path: {self.path}")

        # build directory pattern
        meta_dir_pattern = os.path.join(
            self.path,
            "**",
            "README.md" if self.use_readmes else "")

        # retrieve the list of all sub directories
        all_directories = glob.glob(
            meta_dir_pattern, recursive=True)

        # iterate through directories
        challenges = []
        challenge_unicity = set()

        for directory_path in sorted(all_directories):

            # remove solutions path from directory path
            directory_rel_path = directory_path[len(self.path) + 1:]

            # retrieve challenge match from path
            challenge_match = get_challenge_path(directory_rel_path)

            if challenge_match is None:

                # no match
                continue

            # check whether challenge is known
            if challenge_match in challenge_unicity:

                continue

            # add challenge
            challenge_unicity.add(challenge_match)

            challenge = Challenge(challenge_match)

            challenges.append(challenge)

        # remove nested paths (verify that the path of the challenge is not contained in any of the existing challenge paths)
        sanitized = [c for c in challenges if all(c.path not in p for p in challenge_unicity - set([c.path]))]

        # store challenges
        self.challenges = sanitized


if __name__ == '__main__':

    repo_path = os.path.relpath(os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "..",
        "..",
        "data-solutions"))

    data_dot_syllabus = LookAlikeSyllabus(repo_path, use_readmes=True)

    print(f"loaded data challenges: {len(data_dot_syllabus.challenges)}")

    for challenge in data_dot_syllabus.challenges:

        print(challenge)
