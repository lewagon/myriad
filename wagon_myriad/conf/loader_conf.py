import os

from colorama import Fore, Style

from wagon_myriad.params.params import (
    PROD_ORG, QA_ORG,
    GHA_COURSE_CONVERSION, COURSE_LIST,
    QA_COURSE_ORG, COURSE_ORG, PROD_COURSE_ORG,
    GHA_META_REPOS)

from wagon_myriad.github.auth import load_gh_auth

from wagon_common.helpers.gh.url import GitHubRepo


class LoaderConf:
    """
    loads github auth conf
    determines github organisation, and meta and solutions conf
    """

    def __init__(
            self, gha: bool, organization: str, course: str,
            use_meta_repo: bool = False):

        self.gha = gha
        self.organization = organization
        self.course = course

        # only valid if org is provided
        self.is_prod = self.organization == PROD_ORG
        self.is_qa = self.organization == QA_ORG

        # convert course parameter passed in gha context
        if gha:

            if course not in GHA_COURSE_CONVERSION.keys():

                print(Fore.RED
                      + "\nUnknown course 🤒"
                      + Style.RESET_ALL
                      + f"\n- course: {course}"
                      + f"\n- known courses: {GHA_COURSE_CONVERSION.keys()}")

                raise ValueError(f"Invalid conv course: {course}")

            # convert course
            course = GHA_COURSE_CONVERSION[course]

            # update course
            self.course = course

        # validate parameters
        if course not in COURSE_LIST:

            print(Fore.RED
                  + "\nInvalid course parameter 🤒"
                  + Style.RESET_ALL
                  + f"\ncourse: {course}"
                  + f"\nsupported courses: {' '.join(COURSE_LIST)}")

            raise ValueError(f"Invalid course: {course}")

        # retrieve github organisation
        if self.is_prod:
            org_selector = PROD_COURSE_ORG
        elif self.is_qa:
            org_selector = QA_COURSE_ORG
        else:
            org_selector = COURSE_ORG

        self.myriad_org = org_selector[course]

        # load git and gh credentials from dot env
        self.git_token, self.gh_token = load_gh_auth()

        # build meta and solutions conf
        if not gha:

            if use_meta_repo:
                # The meta repo should be at $HOME/code/lewagon/
                self.meta_repo_path = os.path.relpath(
                    os.path.join(os.getenv('HOME'), 'code', PROD_ORG, f"{course}-meta"))

                self.meta_github_repo = None

            # so the solutions repo
            self.solutions_repo_path = os.path.relpath(
                    os.path.join(os.getenv('HOME'), 'code', PROD_ORG, f"{course}-solutions"))
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
