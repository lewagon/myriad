
from wagon_myriad.loader import Loader

loader = data_local_loader = Loader(
    gha=False, organization="lewagon-test", course="data",
    use_meta_repo=True, use_sol_repo=True,
    use_dot_repo=True, use_lal_repo=True,
    use_md_repo=True, use_gh_repo=True)

# loader = data_local_loader = Loader(course="data", gha=False, prod=False)
# loader = web_local_loader = Loader(course="fullstack", gha=False, prod=False)

# loader = data_gha_loader = Loader(course="data-solutions", gha=True, prod=False)
# loader = web_gha_loader = Loader(course="fullstack-solutions", gha=True, prod=False)

loader.meta_repo

loader.solutions_repo
loader.dot_repo
loader.look_alike_repo
loader.readme_repo

loader.github_repo

# myr list:
# - list meta data syllabus content

# myr gen v1:
# - generate individual challenges through sync v1 - one shot

# myr gen v2:
# - generate individual challenges through sync v2

# myr ver:
# - verify discrepancies (diff in challenges) between
# - github organisation generated challenges and meta repo challenges

# myr meta:
# - generate solutions repo meta directories from meta repo
# - and from params for challenge names with specific rules

# myr synchronized: verify that challenge names are synced
# between meta and dot syllabus,
# between dot and look alike and between look alike and readme repo,
# verify that all challenges have a readme.md

# myr unicity:
# - verify that challenge names are unique
