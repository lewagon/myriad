
import os
import shutil

from colorama import Fore, Style

from wagon_myriad.conf.conf import load_gh_sync_conf, save_gh_sync_conf

from wagon_myriad.github.auth import load_gh_token

from wagon_myriad.params.params import COURSE_ORG, DEFAULT_REMOTE_NAME

from wagon_common.helpers.file import cp

from wagon_common.helpers.git.create import git_init, git_commit
from wagon_common.helpers.git.push import git_push
from wagon_common.helpers.git.status import git_status
from wagon_common.helpers.git.branch import get_current_branch
from wagon_common.helpers.git.remote import git_remote_list, git_remote_add

from wagon_common.helpers.gh.repo import gh_repo_create
from wagon_common.helpers.gh.api.repo import gh_repo_rename
from wagon_common.helpers.gh.api.remote import gh_get_params_from_remote


def generate_challenge_repositories(meta_repo, course, challenges, force):
    """
    legacy one shot sync
    """

    # build repo org
    course_org = COURSE_ORG[course]

    print(Fore.GREEN
          + "\nRetrieve parameters"
          + Style.RESET_ALL
          + f"\n- target gh organisation: {course_org}")

    # build meta repo name
    challenges_repo = os.path.relpath(os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "..",
        f"{course}-challenges"))

    # verify repo existence
    if not os.path.isdir(challenges_repo):

        print(Fore.RED
              + "\nMissing challenges directory 🤒"
              + Style.RESET_ALL
              + "\nPlease clone the repo at the corresponding location"
              + f"\n- expected challenges directory path: {challenges_repo}")

        return None

    print(f"- challenges directory: {challenges_repo}")

    # build myriad repo name
    myriad_repo = os.path.relpath(os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "..",
        f"{course}-myriad"))

    print(f"- myriad directory: {myriad_repo}")

    # verify target repo existence
    if not os.path.isdir(myriad_repo) or force:

        # check whether target should be erased
        if force:

            print(Fore.RED
                  + "\nErase myriad directory"
                  + Style.RESET_ALL
                  + f"\n- erased myriad directory path: {myriad_repo}")

            # erase the target directory
            shutil.rmtree(myriad_repo)

        print(Fore.GREEN
              + "\nCreate myriad directory"
              + Style.RESET_ALL
              + f"\ncopy {challenges_repo} repository to {myriad_repo}")

        # dupicate target challenge structure
        cp(challenges_repo, myriad_repo, recursive=True)

    else:

        print(Fore.BLUE
              + "\nMyriad directory already exists"
              + Style.RESET_ALL)

    # # previous implementation removed git dir

    # # build git repo path
    # git_dir_path = os.path.join(
    #     myriad_repo,
    #     ".git")

    # # remove git repo
    # shutil.rmtree(git_dir_path)

    # # the challenges repo is used in order to
    # # pull the latest version of the challenges during the transition
    # # the added myriad repos gitignores are viewed as untracked
    # # and are not an issue for the git pull commands to complete

    # load gh sync conf
    gh_sync_conf = load_gh_sync_conf(meta_repo)

    # load gh pat
    gh_pat = load_gh_token()

    # iterate through challenges
    for challenge in challenges:

        # get repo name
        future_repo_name = challenge.gh_repo_name(course)

        # check whether challenge gh sync conf exists
        challenge_gh_sync_conf_exists = challenge.path in gh_sync_conf.keys()

        # get challenge gh sync conf
        challenge_sync_conf = gh_sync_conf.get(challenge.path, {})
        gh_sync_conf[challenge.path] = challenge_sync_conf

        # retrieve the existing repo id
        gh_repo_id = challenge_sync_conf.get("repo_id")
        challenge_sync_conf["repo_id"] = gh_repo_id

        # retrieve the existing repo node id
        gh_repo_node_id = challenge_sync_conf.get("repo_node_id")
        challenge_sync_conf["repo_node_id"] = gh_repo_node_id

        # set the expected repo name
        gh_repo_name = future_repo_name
        challenge_sync_conf["repo_target_name"] = gh_repo_name

        # retrieve the existing repo fullname
        gh_repo_fullname = challenge_sync_conf.get("repo_fullname")
        challenge_sync_conf["repo_fullname"] = gh_repo_fullname

        # retrieve the existing repo url
        gh_repo_url = challenge_sync_conf.get("repo_url")
        challenge_sync_conf["repo_url"] = gh_repo_url

        # retrieve the existing repo name
        gh_repo_current_name = challenge_sync_conf.get("repo_current_name")
        challenge_sync_conf["repo_current_name"] = gh_repo_current_name

        # build challenge path
        challenge_path = os.path.join(
            myriad_repo,
            challenge.path)

        print(Fore.BLUE
              + "\nChallenge gh sync conf:"
              + Style.RESET_ALL
              + f"\n- challenge: {challenge.path}"
              + f"\n- target repo: {challenge_path}"
              + f"\n- gh sync conf exists: {challenge_gh_sync_conf_exists}"
              + f"\n- gh repo id: {gh_repo_id}"
              + f"\n- gh repo node id: {gh_repo_node_id}"
              + f"\n- gh repo name: {gh_repo_name}"
              + f"\n- gh repo fullname: {gh_repo_fullname}"
              + f"\n- gh repo url: {gh_repo_url}"
              + f"\n- gh repo current name: {gh_repo_current_name}")

        print(Fore.BLUE
              + "\nMyriad repo status:"
              + Style.RESET_ALL
              + f"\n- repo: {challenge_path}")

        # build challenge .gitignore path
        challenge_gitignore_path = os.path.join(
            challenge_path,
            ".gitignore")

        if os.path.isfile(challenge_gitignore_path):

            print("- .gitignore exists")

        else:

            # build root gitignore path
            root_gitignore_path = os.path.join(
                myriad_repo,
                ".gitignore")

            # copy root gitignore to challenge
            cp(root_gitignore_path, challenge_path)

            print(Fore.GREEN
                  + "- .gitignore added"
                  + Style.RESET_ALL)

        # build challenge .git path
        challenge_git_path = os.path.join(
            challenge_path,
            ".git")

        if os.path.isdir(challenge_git_path):

            print("- .git exists")

            commit_message = "new commit from myriad 🍇"

        else:

            print(Fore.GREEN
                  + "- init the git repository"
                  + Style.RESET_ALL)

            # create git repo
            rc, output, error = git_init(challenge_path)

            if rc != 0:

                print(Fore.RED
                      + "\nUnable to init git repo for challenge 🥺"
                      + Style.RESET_ALL
                      + f"\n- return code: {rc}"
                      + f"\n- output: {output}"
                      + f"\n- error: {error}")

                return

            commit_message = "initial commit from myriad 🍇"

        clean_status = git_status(challenge_path)

        if clean_status:

            print("- clean git status, nothing to commit")

        else:

            print(Fore.GREEN
                  + "- create new commit"
                  + Style.RESET_ALL)

            # commit everything
            (rc, rc2), (output, output2), (error, error2) \
                = git_commit(
                    challenge_path,
                    commit_message)

            if rc != 0:

                print(Fore.RED
                      + "\nUnable to commit individual challenge repo 😬"
                      + Style.RESET_ALL
                      + f"\n- add return code: {rc}"
                      + f"\n- add output: {output}"
                      + f"\n- add error: {error}"
                      + f"\n- commit return code: {rc2}"
                      + f"\n- commit output: {output2}"
                      + f"\n- commit error: {error2}")

                return

        # check if remote exists
        remotes = git_remote_list(challenge_path)

        has_no_remotes = len(remotes) == 0

        if has_no_remotes:
            remote_name = DEFAULT_REMOTE_NAME
        else:
            remote_name = remotes[0]

        print(Fore.BLUE
              + "\nMyriad remote status:"
              + Style.RESET_ALL
              + f"\n- repo: {challenge_path}")

        # check whether a gh sync conf exists for challenge
        if challenge_gh_sync_conf_exists:

            # a gh sync conf preexists with gh repo id, name and url
            # which are supposed to be valid

            # check if a remote already exists
            if has_no_remotes:

                print(Fore.GREEN
                      + f"- add remote for existing gh sync conf repo id {gh_repo_id}"
                      + Style.RESET_ALL)

                # add remote
                rc, output, error = git_remote_add(challenge_path, remote_name, gh_repo_url)

                if rc != 0:

                    print(Fore.RED
                          + "\nUnable to add remote"
                          + Style.RESET_ALL
                          + f"\n- repo id: {gh_repo_id}"
                          + f"\n- rc: {rc}"
                          + f"\n- output: {output}"
                          + f"\n- error: {error}")

            else:

                print("- remote exists for gh sync conf")

                # nothing to do

            # retrieve existing repo id and name from gh
            res_gh_repo_id, res_gh_repo_node_id, gh_repo_current_name, gh_repo_fullname, gh_repo_url = gh_get_params_from_remote(challenge_path, remote_name, gh_pat)

            # check remote info
            if gh_repo_id != res_gh_repo_id:

                print(Fore.RED
                      + "\nRemote id does not match the gh sync conf id"
                      + Style.RESET_ALL
                      + f"\n- expected gh repo id: {gh_repo_id}"
                      + f"\n- expected gh repo name: {gh_repo_name}"
                      + f"\n- expected gh repo url: {gh_repo_url}"
                      + f"\n- remote gh repo id: {res_gh_repo_id}"
                      + f"\n- remote gh repo name: {gh_repo_current_name}"
                      + f"\n- remote gh repo url: {gh_repo_url}"
                      + f"\n- challenge: {rc}")

                return

            else:

                print("- remote gh repo id matches gh sync conf")

        else:

            # check if a remote already exists
            if has_no_remotes:

                # no gh sync conf exists and there is no remote
                # create a new gh repo

                # TODO 🔥 🔥 🔥
                # check case where remote does not exist for gh repo does
                # and there is no gh sync conf info
                # because the command failed for some reason after gh repo creation
                # and remote was not created
                # currently the solution is to delete the gh repo

                print(Fore.GREEN
                      + "- create gh repo"
                      + Style.RESET_ALL)

                # build repo fullname
                repo_fullname = f"{course_org}/{gh_repo_name}"

                # create gh repo
                rc, output, error = gh_repo_create(
                    challenge_path,
                    repo_fullname)

                if rc != 0:

                    print(Fore.RED
                          + "\nUnable to create gh repo for challenge 🤕"
                          + Style.RESET_ALL
                          + f"\n- return code: {rc}"
                          + f"\n- output: {output}"
                          + f"\n- error: {error}")

                    return

            else:

                print("- remote already exists without gh sync conf")

            # retrieve existing gh repo name and repo id from existing remote
            # in order to store in gh sync conf

            # retrieve existing repo id and name from gh
            res_gh_repo_id, res_gh_repo_node_id, gh_repo_current_name, gh_repo_fullname, gh_repo_url = gh_get_params_from_remote(challenge_path, remote_name, gh_pat)

        # gh repo name should not need to be updated
        # challenge_sync_conf["repo_target_name"] = gh_repo_name

        # update gh sync conf with retrieved remote data
        challenge_sync_conf["repo_id"] = res_gh_repo_id
        challenge_sync_conf["repo_node_id"] = res_gh_repo_node_id
        challenge_sync_conf["repo_url"] = gh_repo_url
        challenge_sync_conf["repo_fullname"] = gh_repo_fullname
        challenge_sync_conf["repo_current_name"] = gh_repo_current_name

        # retrieve current branch
        rc, output, error, current_branch = get_current_branch(challenge_path)

        if rc != 0:

            print(Fore.RED
                  + "\nUnable to determine individual repo current branch 🙃"
                  + Style.RESET_ALL
                  + f"\n- return code: {rc}"
                  + f"\n- output: {output}"
                  + f"\n- error: {error}")

            return

        print(f"- current branch: {current_branch}")

        print("- push code to gh repo")

        # push code
        rc, output, error = git_push(challenge_path, current_branch)

        if rc != 0:

            print(Fore.RED
                  + "\nUnable to push individual repo code ☹️"
                  + Style.RESET_ALL
                  + f"\n- return code: {rc}"
                  + f"\n- output: {output}"
                  + f"\n- error: {error}")

            return

        # check gh repo name
        if gh_repo_name != gh_repo_current_name:

            # update repo name
            gh_repo_rename(gh_repo_fullname, gh_repo_name, gh_pat)

            if rc != 0:

                print(Fore.RED
                      + "\nUnable to rename repo 🤕"
                      + Style.RESET_ALL
                      + f"\n- return code: {rc}"
                      + f"\n- output: {output}"
                      + f"\n- error: {error}")

                return

            print(Fore.GREEN
                  + f"- rename repo from: {gh_repo_current_name} to: {gh_repo_name}"
                  + Style.RESET_ALL)

    # save gh sync conf
    save_gh_sync_conf(meta_repo, gh_sync_conf)
