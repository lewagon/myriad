
from wagon_common.helpers.git.diff import git_diff_filenames

from pathlib import Path
import re


def list_commited_challenges(challenges, path, ref, verbose):
    """
    return a list of challenges impacted by the current commits
    """

    # retrieve commits filenames
    filenames = git_diff_filenames(
        path=path, branch=ref, verbose=verbose)

    # iterate through files
    challenge_paths = set()

    for file_path in filenames:

        # get challenge path
        challenge_path = get_challenge_path(file_path)

        # check if there is a match
        if challenge_path is not None:

            # append to challenge paths
            challenge_paths.add(challenge_path)

    # identify challenges impacted by commits
    impacted_challenges = [c for c in challenges if c.path in challenge_paths]

    return impacted_challenges


def get_challenge_path(file_path):
    """
    return challenge path in file path from directory structure
    supported challenge paths:
    - 01-Staff/01-Steff/01-Stiff/some/content/there.md
    - 01-Staff/01-Steff/Optional-Stiff/some/content/there.md
    - 01-Staff/01-Steff/Reboot-Stiff/some/content/there.md
    - 01-Staff/01-Steff/Reboot/some/content/there.md
    - 01-Staff/01-Steff/Recap/some/content/there.md
    - 01-Staff/01-Steff/some/content/there.md
    """

    # retrieve challenge path using directory structure
    re_pattern = r"(\d\d-[^\/]*\/\d\d-[^\/]*\/\d\d-[^\/]*)|(\d\d-[^\/]*\/\d\d-[^\/]*\/Recap)|(\d\d-[^\/]*\/\d\d-[^\/]*\/Reboot[^\/]*)|(\d\d-[^\/]*\/\d\d-[^\/]*\/Optional-[^\/]*)|(\d\d-[^\/]*\/\d\d-[^\/]*)"
    compiled_re = re.compile(re_pattern)
    matches = compiled_re.match(file_path)

    # verify if filename is in a challenge
    if matches is None:

        # retrieve challenge path using metadata file
        return get_challenge_root(file_path)

    # retrieve valid match
    challenge_path = [e for e in matches.groups() if e is not None][0]

    return challenge_path


def get_challenge_root(file_path):
    """
    return challenge path in file path from the location of the metadata file
    supported challenge paths:
    - **/some/content/there.md (where **/ contains `.lewagon/metadata.yml`)
    """

    # look for the metadata file from the bottom of the path
    path = Path(file_path)

    # search all directories in the path upwards and one at a time
    while(path != path.parent):

        # check if the current path is a challenge
        if path.joinpath(".lewagon", "metadata.yml").is_file():

            # current path is a challenge
            return str(path)

        # switch to parent directory
        path = path.parent

    # no challenge found in the path
    return None


if __name__ == '__main__':

    from colorama import Fore, Style

    from wagon_myriad.params.params import COURSE_DATA

    from wagon_myriad.loader import Loader

    loader = Loader(
        course=COURSE_DATA,
        use_meta_repo=True)

    impacted_challenges = list_commited_challenges(
        loader.meta_repo.syllabus.challenges,
        "../../data-solutions",
        "upstream/master",
        verbose=False)

    print(Fore.BLUE
          + "\nImpacted challenges:"
          + Style.RESET_ALL)

    for challenge in impacted_challenges:
        print(challenge.path)

    # testing challenge path
    print(Fore.GREEN
          + "\nTesting path match:"
          + Style.RESET_ALL)

    for path in [
        "01-Staff/01-Steff/01-Stiff/some/content/there.md",
        "01-Staff/01-Steff/Optional-Stiff/some/content/there.md",
        "01-Staff/01-Steff/Reboot-Stiff/some/content/there.md",
        "01-Staff/01-Steff/Reboot/some/content/there.md",
        "01-Staff/01-Steff/Recap/some/content/there.md",
        "01-Staff/01-Steff/some/content/there.md",
    ]:

        print(Fore.BLUE
              + "\nMatches for:"
              + Style.RESET_ALL
              + f"\n- path: {path}"
              + f"\n- match: {get_challenge_path(path)}")
