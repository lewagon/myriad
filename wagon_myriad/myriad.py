
from wagon_common.helpers.gh.api.fetch import fetch_repos
from wagon_myriad.conf.conf import load_gh_sync_conf

from wagon_myriad.params.params import COURSE_ORG

from wagon_myriad.github.auth import load_gh_token


def check_meta_vs_myriad(course, meta_repo):
    """
    check discrepancies between myriad repo and meta repo gh sync yaml
    """

    # load gh sync conf
    gh_sync_conf = load_gh_sync_conf(meta_repo)

    # build repo org
    course_org = COURSE_ORG[course]

    # load gh pat
    gh_pat = load_gh_token()

    # load myriad repos
    repos = fetch_repos(course_org, gh_pat)

    # filter interests
    interests = [
        "id",
        "node_id",
        "name",
        "fullname",
        "html_url",
        "private",
        "updated_at"]   # last commit date

    # filter retrieved fields
    filtered_repos = [{k: v for k, v in r.items() if k in interests} for r in repos]

    return gh_sync_conf, filtered_repos
