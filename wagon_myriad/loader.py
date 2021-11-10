
from wagon_myriad.params.params import COURSE_DATA

from wagon_myriad.conf.loader_conf import LoaderConf

from wagon_myriad.repositories.meta_repository import MetaRepository

from wagon_myriad.repositories.solutions_repository import SolutionsRepository
from wagon_myriad.repositories.dot_repository import DotRepository
from wagon_myriad.repositories.look_alike_repository import LookAlikeRepository
from wagon_myriad.repositories.readme_repository import ReadmeRepository

from wagon_myriad.repositories.github_org_repository import GithubOrgRepository


class Loader:

    def __init__(
            self, gha: bool = False, organization: str = None, course: str = COURSE_DATA,
            gh_nickname: str = None, gh_token: str = None,
            use_meta_repo: bool = False, use_sol_repo: bool = False,
            use_dot_repo: bool = False, use_lal_repo: bool = False,
            use_md_repo: bool = False, use_gh_repo: bool = False):

        self.loader_conf = lc = LoaderConf(
            gha=gha, organization=organization, course=course,
            gh_nickname=gh_nickname, gh_token=gh_token,
            use_meta_repo=use_meta_repo)

        if use_meta_repo:
            self.meta_repo = MetaRepository(lc.meta_repo_path, lc.meta_github_repo)

        if use_sol_repo:
            self.solutions_repo = SolutionsRepository(lc.solutions_repo_path)

        if use_dot_repo:
            self.dot_repo = DotRepository(lc.solutions_repo_path)

        if use_lal_repo:
            self.look_alike_repo = LookAlikeRepository(lc.solutions_repo_path)

        if use_md_repo:
            self.readme_repo = ReadmeRepository(lc.solutions_repo_path)

        if use_gh_repo:
            # this does not make sense anymore since the sync repo fullnames
            # are now listed in the challenge metadata
            self.github_repo = GithubOrgRepository(lc.myriad_org)
