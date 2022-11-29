
import os

from colorama import Fore, Style

from wagon_myriad.params.params import (
    PROD_ORG,
    GHA_COURSE_CONVERSION,
    COURSE_ORG, PROD_COURSE_ORG,
    GHA_META_REPOS)

from wagon_myriad.params.git import GHA_GIT_USER_NAME, GHA_GIT_USER_EMAIL

from wagon_myriad.github.auth import load_gh_auth

from wagon_common.helpers.gh.url import GitHubRepo


class LoaderConf:
    """
    loads github auth conf
    determines github organisation, and meta and solutions conf
    """

    def __init__(
            self, gha: bool, organization: str, course: str,
            gh_nickname: str, gh_token: str,
            use_meta_repo: bool = False):

        self.gha = gha
        self.organization = organization
        self.course = course

        # only valid if org is provided
        self.is_prod = self.organization == PROD_ORG

        # convert course parameter passed in gha context
        if gha:

            if course not in GHA_COURSE_CONVERSION.keys():

                print(Fore.RED
                      + "\nUknown course 🤒"
                      + Style.RESET_ALL
                      + f"\n- course: {course}"
                      + f"\n- known courses: {GHA_COURSE_CONVERSION.keys()}")

                raise ValueError(f"Invalid course: {course}")

            # convert course
            course = GHA_COURSE_CONVERSION[course]

            # update course
            self.course = course

        # validate parameters
        if course not in PROD_COURSE_ORG.keys():

            print(Fore.RED
                  + "\nInvalid course parameter 🤒"
                  + Style.RESET_ALL
                  + f"\ncourse: {course}"
                  + f"\nsupported courses: {' '.join(PROD_COURSE_ORG.keys())}")

            raise ValueError(f"Invalid course: {course}")

        # retrieve github organisation
        org_selector = PROD_COURSE_ORG if self.is_prod else COURSE_ORG

        self.myriad_org = org_selector[course]

        # handle git and gh credentials
        if gha:

            # set git params for gha
            self.git_user_name = GHA_GIT_USER_NAME
            self.git_user_email = GHA_GIT_USER_EMAIL

            # stored gh nickname and token from params
            self.gh_nickname = gh_nickname
            self.gh_token = gh_token

        else:

            # load git and gh params from dot env
            (
                self.git_user_name,
                self.git_user_email,
                self.gh_nickname,
                self.gh_token) = load_gh_auth()

        # build meta and solutions conf
        if not gha:

            if use_meta_repo:

                # the meta repo is expected to be there
                self.meta_repo_path = os.path.relpath(os.path.join(
                    os.path.dirname(__file__),
                    "..", "..", "..", "..",
                    f"{course}-meta"))

                self.meta_github_repo = None

            # so is the solutions repo
            self.solutions_repo_path = os.path.relpath(os.path.join(
                os.path.dirname(__file__),
                "..", "..", "..", "..",
                f"{course}-solutions"))

        else:

            # the meta repo needs to be cloned
            meta_org, meta_repo = GHA_META_REPOS[course]

            if use_meta_repo:

                self.meta_repo_path = os.path.relpath(os.path.join(
                    "..",
                    meta_repo))

                self.meta_github_repo = GitHubRepo(
                    org=meta_org,
                    repo=meta_repo,
                    token=self.gh_token)

                self.meta_github_repo.clone(self.meta_repo_path)

            # the gha is ran from within the solutions repo cloned by the gha checkout action
            self.solutions_repo_path = "."
