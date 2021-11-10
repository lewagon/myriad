
import re

from colorama import Fore, Style

from wagon_myriad.params.renaming import CHALLENGE_RENAMING
from wagon_myriad.utils.num_2_words import num_2_words


class Challenge:

    def __init__(self, path):

        self.path = path

    def __repr__(self):

        return (
            "#<Challenge "
            f"path={self.path} "
            f"@={id(self)}>")

    def suffix(self, name):
        """
        retrieve suffix if name matches 01-Stuff
        - 01-Check => check
        - Recap => recap
        """

        # extract suffix
        re_pattern = r"\d\d-(.*)"
        compiled_re = re.compile(re_pattern)
        matches = compiled_re.match(name)

        # check matches
        if matches is not None:
            return matches[1].lower()

        return name.lower()

    def prefix(self, name):
        """
        retrieve prefix if name matches 01-Stuff
        - 01-Check => 01
        - Recap => None
        """

        # extract prefix
        re_pattern = r"(\d\d)-.*"
        compiled_re = re.compile(re_pattern)
        matches = compiled_re.match(name)

        # check matches
        if matches is not None:
            return int(matches[1].lower())

        return None

    def gh_repo_name(
            self,
            course,
            use_challenge=False,
            use_mod_cha=False,
            use_sub_number=False,
            verbose=False):
        """
        process the gh repo name from the challenge path
        """

        # build module, submodule and challenge from path
        module = self.suffix(self.path.split("/")[0])
        submodule_raw = self.path.split("/")[-2:][0]
        submodule = self.suffix(submodule_raw)
        challenge = self.suffix(self.path.split("/")[-1])

        # build canonical repo name
        canonical_repo_name = (
            course
            + "-"
            + "-".join([n[:2] for n in self.path.split("/")[:-1]])
            + "-"
            + self.path.split("/")[-1:][0]).lower()

        # build sub number word
        subprefix = self.prefix(submodule_raw)
        subnumber_word = num_2_words(subprefix) if subprefix is not None else "none"

        # build repo names
        course_challenge = f"{course}-{challenge}"
        module_challenge = f"{module}-{challenge}"
        module_subnumber_challenge = f"{module}-{subnumber_word}-{challenge}"
        module_submodule_challenge = f"{module}-{submodule}-{challenge}"

        # select repo name
        target_repo_name = module_submodule_challenge

        # if course == COURSE_WEB:

        #     target_repo_name = module_challenge

        if verbose:

            print(Fore.BLUE
                  + "\nChallenge params:"
                  + Style.RESET_ALL
                  + f"\n- course: {course}"
                  + f"\n- path: {self.path}"
                  + f"\n- module: {module}"
                  + f"\n- submodule: {submodule}"
                  + f"\n- challenge: {challenge}"
                  + f"\n- canonical: {canonical_repo_name}"
                  + f"\n- course challenge: {course_challenge}"
                  + f"\n- module challenge: {module_challenge}"
                  + f"\n- module subnumber challenge: {module_subnumber_challenge}"
                  + f"\n- module submodule challenge: {module_submodule_challenge}"
                  + f"\n- target repo name: {target_repo_name}")

        # use challenge renaming
        challenge_renamings = CHALLENGE_RENAMING.get(course, {})

        if self.path in challenge_renamings.keys():
            return challenge_renamings[self.path]

        # option to return challenge as repo name
        if use_challenge:
            return challenge

        # option to return module subnumber challenge as repo name
        if use_sub_number:
            return module_subnumber_challenge

        # option to return module challenge as repo name
        if use_mod_cha:
            return module_challenge

        return target_repo_name
