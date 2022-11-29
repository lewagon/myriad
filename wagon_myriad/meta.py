
import os

from colorama import Fore, Style

from wagon_myriad.params.params import (
    COURSE_LIST,
    PROD_COURSE_ORG,
    BRANCH_VERBOSE,
    BRANCH_MYRIAD_FORCE,
    BRANCH_MYRIAD_OVERWRITE,
    GHA_EVENT_PUSH)

from wagon_myriad.params.branch import extract_overwrite_sha

from wagon_myriad.params.meta import (
    SOLUTION_META_DIRECTORY,
    SOLUTION_META_FILE,
    SOLUTION_META_CHALLENGE_OUTPUT)

from wagon_myriad.loader import Loader

from wagon_myriad.models.repo.yaml_file import YamlFile
from wagon_myriad.github.context import list_commited_challenges
# from wagon_myriad.github.github_sync import generate_challenge_repositories
from wagon_myriad.github.gha_sync import gha_generate_challenge_repositories
from wagon_myriad.myriad import check_meta_vs_myriad
from wagon_myriad.refacto import sanity_check_report


def gen_challenge_repos(
        event, syllabus, is_prod, is_qa,
        solutions_repo_path,
        head_ref, base_ref, base_commit,
        git_token, gh_token,
        remote, param_verbose, force):
    """
    generate individual challenge repositories from course repo
    """

    # check syllabus
    if syllabus.challenges is None:

        exit(1)

    # identify the challenges to sync
    impacted_challenges = syllabus.challenges

    # retrieve verbose option
    verbose = BRANCH_VERBOSE in head_ref or param_verbose

    # retrieve option to force in gha pr branch name
    if BRANCH_MYRIAD_FORCE in head_ref:

        print(Fore.BLUE
              + "\nBranch name contains option to force the generation of all challenges"
              + Style.RESET_ALL
              + f"\n- head ref: {head_ref}")

        force = True

    # retrieve the challenges impacted by github commits
    if force:

        print(Fore.BLUE
              + "\nForce the generation of all challenges"
              + Style.RESET_ALL)

        # generate all challenges
        impacted_challenges = syllabus.challenges

    else:

        # select reference for diff
        if event == GHA_EVENT_PUSH:

            # gha push: use the last commit before the pushed code as ref
            ref = base_commit

        else:

            # gha pr: use the base branch
            ref = f"{remote}/{base_ref}"

        # list impacted challenges
        impacted_challenges = list_commited_challenges(
            challenges=syllabus.challenges,
            path=".",
            ref=ref,
            verbose=verbose)

    print(Fore.BLUE
          + "\nImpacted challenges:"
          + Style.RESET_ALL)

    # output
    print("\n".join([f"- {c.path}" for c in impacted_challenges]))

    # retrieve option to overwrite individual challenges
    overwrite_sha = None

    if BRANCH_MYRIAD_OVERWRITE in head_ref:

        overwrite_sha = extract_overwrite_sha(head_ref)

    # generate repositories
    gha_generate_challenge_repositories(
        event=event, challenges=impacted_challenges,
        base_ref=base_ref, is_prod=is_prod, is_qa=is_qa,
        solutions_repo_path=solutions_repo_path,
        git_token=git_token, gh_token=gh_token,
        overwrite_sha=overwrite_sha,
        verbose=verbose)

    # # legacy one shot sync based
    # generate_challenge_repositories(
    #     syllabus.meta_repo, course, impacted_challenges, force)


def check_sync():
    """
    check discrepancies between myriad repo and meta repo gh sync yaml
    """

    # iterate through courses
    global_conf = []
    global_repos = []

    for course in COURSE_LIST:

        # retrieve syllabus
        loader = Loader(
            course=course, gha=False,
            use_meta_repo=True)

        # check sync
        gh_sync_conf, repos = check_meta_vs_myriad(
            course, loader.meta_repo.path)

        # append course
        conf_repos = [dict(**r, course=course, path=p) for p, r in gh_sync_conf.items()]
        org_repos = [dict(**r, course=course) for r in repos]

        # store results
        global_conf += conf_repos
        global_repos += org_repos

    # retrieve conf repos
    conf_repos = set([r["repo_id"] for r in global_conf])

    # retrieve org repos
    org_repos = set([r["id"] for r in global_repos])

    # select org repos not in gh sync conf repos
    org_repos_not_in_conf = org_repos - conf_repos

    # select gh sync conf repos not in org repos
    conf_repos_not_in_org = conf_repos - org_repos

    # show repos in org but not in conf
    if len(org_repos_not_in_conf) > 0:

        print(Fore.RED
              + "\nOrg repos not in conf"
              + Style.RESET_ALL)

        for weird_repo in org_repos_not_in_conf:

            wrepo = [r for r in global_repos if r["id"] == weird_repo]

            print(wrepo)

    else:

        print(Fore.GREEN
              + "\nNo org repos not in conf 🎉"
              + Style.RESET_ALL)

    # show unsync repos
    if len(conf_repos_not_in_org) > 0:

        print(Fore.RED
              + "\nConf repos not in org"
              + Style.RESET_ALL)

        for unsynced_repo in conf_repos_not_in_org:

            urepo = [r for r in global_conf if r["repo_id"] == unsynced_repo]

            print(urepo)

    else:

        print(Fore.GREEN
              + "\nNo unsynced repos 🎉"
              + Style.RESET_ALL)


def generate_meta(syllabus, course, force):
    """
    generate meta directories and default files in individual solutions
    """

    # build repo org
    prod_course_org = PROD_COURSE_ORG[course]

    # build solutions repo name
    solutions_repo = os.path.relpath(os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        f"{course}-solutions"))

    # verify repo existence
    if not os.path.isdir(solutions_repo):

        print(Fore.RED
              + "\nMissing solutions directory 🤒"
              + Style.RESET_ALL
              + "\nPlease clone the repo at the corresponding location"
              + f"\n- expected solutions directory path: {solutions_repo}")

        return None

    print(Fore.GREEN
          + "\nRetrieve parameters"
          + Style.RESET_ALL
          + f"\n- prod course org: {prod_course_org}"
          + f"\n- solutions directory: {solutions_repo}")

    print(Fore.BLUE
          + "\nCreate meta directories"
          + Style.RESET_ALL)

    # identify duplicate repo names
    # this is required since we want to name duplicate repos
    # - module-one-recap
    # - module-two-recap
    # and not
    # - module-recap
    # - module-two-recap
    initial_gh_repo_names = {}

    for challenge in syllabus.challenges:

        # retrieve challenge repo name
        verbose = False  # display repo name building options
        repo_full_name = challenge.gh_repo_name(
            course,
            use_challenge=True,
            # use_mod_cha=True,         # use challenge as repo name
            # use_sub_number=False,     # use challenge as repo name
            verbose=verbose)

        # append set
        repo_challenges = initial_gh_repo_names.get(repo_full_name, [])
        repo_challenges.append(challenge)
        initial_gh_repo_names[repo_full_name] = repo_challenges

    # mark challenges with duplicate repo names
    for repo_full_name, dup_challenges in initial_gh_repo_names.items():

        # mark challenges
        for dup_challenge in dup_challenges:
            dup_challenge.has_duplicate_default_repo = len(dup_challenges) > 1

    # build repo names collection
    gh_repo_names = {}

    # iterate through challenges
    for challenge in syllabus.challenges:

        # build solution meta dir path
        solution_meta_dir = os.path.relpath(os.path.join(
            solutions_repo,
            challenge.path,
            SOLUTION_META_DIRECTORY))

        # build solution meta file path
        solution_meta_file = os.path.relpath(os.path.join(
            solution_meta_dir,
            SOLUTION_META_FILE))

        print(f"- {solution_meta_file}: ", end="")

        # verify meta directory existence
        if not os.path.isdir(solution_meta_dir):

            # create directory
            os.makedirs(solution_meta_dir)

            print(Fore.GREEN
                  + " +"
                  + Style.RESET_ALL,
                  end="")

        else:

            print(Fore.BLUE
                  + " x"
                  + Style.RESET_ALL,
                  end="")

        # check whether repo name is duplicate
        repo_name_is_duplicate = challenge.has_duplicate_default_repo

        # retrieve challenge repo name
        verbose = False  # display repo name building options
        repo_full_name = challenge.gh_repo_name(
            course,
            use_challenge=True,
            # use_mod_cha=True,                             # use challenge as repo name
            # use_sub_number=repo_name_is_duplicate,        # use challenge as repo name
            verbose=verbose)

        # build challenge gh repo full name
        sol_gh_repo_full_name = f"{prod_course_org}/{repo_full_name}"

        # append set
        repo_challenges = gh_repo_names.get(sol_gh_repo_full_name, [])
        repo_challenges.append(challenge)
        gh_repo_names[sol_gh_repo_full_name] = repo_challenges

        # verify meta file existence
        if not os.path.isfile(solution_meta_file):

            # create content
            meta_content = {
                    SOLUTION_META_CHALLENGE_OUTPUT: sol_gh_repo_full_name
                }

            # create file
            dot_meta_file = YamlFile(solution_meta_file)
            dot_meta_file.save(meta_content)

            print(Fore.GREEN
                  + " +"
                  + Style.RESET_ALL)

        else:

            dot_meta_file = YamlFile(solution_meta_file)
            existing_meta_content = dot_meta_file.load()

            # set output if it is not defined
            challenge_output = existing_meta_content.get(SOLUTION_META_CHALLENGE_OUTPUT, sol_gh_repo_full_name)

            # overwrite existing value
            if force:
                challenge_output = sol_gh_repo_full_name

            # save value
            existing_meta_content[SOLUTION_META_CHALLENGE_OUTPUT] = challenge_output

            # write file
            dot_meta_file.save(existing_meta_content)

            print(Fore.BLUE
                  + " x"
                  + Style.RESET_ALL)

    sanity_check_report(gh_repo_names, syllabus.challenges)


def sylls_challenges_sanity_check(meta_syllabus, dot_syllabus, lal_syllabus, mdlal_syllabus):

    meta_paths = {c.path for c in meta_syllabus.challenges}
    dot_paths = {c.path for c in dot_syllabus.challenges}
    lal_paths = {c.path for c in lal_syllabus.challenges}
    mdlal_paths = {c.path for c in mdlal_syllabus.challenges}

    print(Fore.GREEN
          + "\nSanity check meta syllabus vs dot syllabus:"
          + Style.RESET_ALL
          + f"\n- meta syllabus length: {len(meta_syllabus.challenges)}"
          + f"\n- dot syllabus length: {len(dot_syllabus.challenges)}"
          + f"\n- look alike syllabus length: {len(lal_syllabus.challenges)}"
          + f"\n- look alike md syllabus length: {len(mdlal_syllabus.challenges)}"
          + f"\n- meta syllabus uniques: {len(meta_paths)}"
          + f"\n- dot syllabus uniques: {len(dot_paths)}"
          + f"\n- look alike syllabus uniques: {len(lal_paths)}"
          + f"\n- look alike syllabus uniques: {len(mdlal_paths)}")

    # process sync issues between meta and dot
    meta_not_in_dot = [c for c in meta_syllabus.challenges if c.path not in dot_paths]
    dot_not_in_meta = [c for c in dot_syllabus.challenges if c.path not in meta_paths]

    # process sync issues between dot and lal
    dot_not_in_lal = [c for c in dot_syllabus.challenges if c.path not in lal_paths]
    lal_not_in_dot = [c for c in lal_syllabus.challenges if c.path not in dot_paths]

    # process sync issues between lal and mdlal
    lal_not_in_mdlal = [c for c in lal_syllabus.challenges if c.path not in mdlal_paths]
    mdlal_not_in_lal = [c for c in mdlal_syllabus.challenges if c.path not in lal_paths]

    # iterate through comparisons
    for a_not_in_b, syll_a, syll_b in [
        (meta_not_in_dot, "meta", "dot"),
        (dot_not_in_meta, "dot", "meta"),
        (dot_not_in_lal, "dot", "lal"),
        (lal_not_in_dot, "lal", "dot"),
        (lal_not_in_mdlal, "lal", "mdlal"),
        (mdlal_not_in_lal, "mdlal", "lal"),
    ]:

        # check match
        if len(a_not_in_b) == 0:

            print(Fore.GREEN
                  + f"\nAll {syll_a} challenges are in {syll_b} 🎉"
                  + Style.RESET_ALL)

        else:

            print(Fore.RED
                  + f"\n{syll_a.capitalize()} challenges not in {syll_b} 😭"
                  + Style.RESET_ALL)

            for challenge in a_not_in_b:

                print(f"- {challenge.path}")

    # challenges referenced in the program without a readme
    refed_without_a_readme = [c for c in lal_not_in_mdlal if c.path in dot_paths]

    # check match
    if len(refed_without_a_readme) == 0:

        print(Fore.GREEN
              + "\nAll challenges referenced in the program have a README.md 🎉"
              + Style.RESET_ALL)

    else:

        print(Fore.RED
              + "\nChallenges referenced in the program without a README.md 😭"
              + Style.RESET_ALL)

        for challenge in refed_without_a_readme:

            print(f"- {challenge.path}")
