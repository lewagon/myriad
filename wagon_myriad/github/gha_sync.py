
import os

from colorama import Fore, Style

from wagon_myriad.params.params import (
    TEST_ORG, DEFAULT_REMOTE_NAME, GHA_EVENT_PULL_REQUEST)

from wagon_myriad.services.challengify_service import challengify_service

from wagon_myriad.params.challengify import CHALLENGIFY_TARGET_PREFIX

from wagon_common.helpers.file import cp, mv

from wagon_common.helpers.gh.api.repo import (
    gh_repo_list,
    gh_api_repo_create,
    gh_api_repo_update)
from wagon_common.helpers.gh.auth import gh_auth
from wagon_common.helpers.gh.url import GitHubRepo
from wagon_common.helpers.gh.url import github_url

from wagon_common.helpers.git.remote import git_remote_add
from wagon_common.helpers.git.create import git_init, git_add, git_commit
from wagon_common.helpers.git.push import git_push
from wagon_common.helpers.git.config import git_config
from wagon_common.helpers.git.commit import get_latest_commit
from wagon_common.helpers.git.checkout import checkout_branch
from wagon_common.helpers.git.branch import rename_branch


def gha_generate_challenge_repositories(
        event, challenges,
        base_ref, is_prod,
        solutions_repo_path,
        git_user_name, git_user_email,
        gh_nickname, gh_token,
        overwrite_sha=None,
        verbose=False):
    """
    gha sync
    """

    print("\nSteps:"
          + "\n- auth to gh")

    # conf gh auth
    conf_gh_auth(git_user_name, git_user_email, gh_nickname, gh_token)

    # overwrite sha
    if overwrite_sha is not None:

        print("- checkout overwrite sha")

        # checkout commit
        is_ok, output, error = checkout_branch(
            solutions_repo_path, overwrite_sha, verbose=verbose)

        if not is_ok:

            print(Fore.RED
                  + "\nUnable to checkout overwrite sha 🥺"
                  + Style.RESET_ALL
                  + f"\n- result: {is_ok}"
                  + f"\n- output: {output}"
                  + f"\n- error: {error}")

            exit(1)

    # iterate through challenges
    for challenge in challenges:

        # overwrite challenge gh repo target if not in prod
        if not is_prod:

            # overwrite challenge meta
            challenge.github_nickname = TEST_ORG
            challenge_name = challenge.challenge_output.split("/")[1]
            challenge.challenge_output = f"{TEST_ORG}/{challenge_name}"

        print(Fore.BLUE
              + "\nSync challenge:"
              + Style.RESET_ALL
              + f"\n- path: {challenge.path}"
              + f"\n- target repo: {challenge.challenge_output}")

        # check whether repo exists
        repo = gh_repo_list(
            challenge.challenge_output, token=gh_token)

        # overwrite sha
        if overwrite_sha is not None:

            # ignore existing repo content
            overwrite_sha_repo_exists = repo is not None
            repo = None

        if repo is not None:

            print("- repo exists")

            # build repo path
            repo_path = challenge.path

            print("- clone repo")

            # build repo path
            cloned_repo_name = challenge.challenge_output.replace("/", "_")
            cloned_repo_path = os.path.abspath(os.path.join(
                "..",
                cloned_repo_name))

            challenge_github_repo = GitHubRepo(
                org=challenge.github_nickname, repo=challenge.repo_name,
                username=gh_nickname, token=gh_token)

            challenge_github_repo.clone(cloned_repo_path, verbose=verbose)

            print("- move cloned repo .git dir")

            # build cloned git dir path
            cloned_git_dir_path = os.path.join(
                cloned_repo_path,
                ".git")

            # move cloned repo git dir
            mv(
                cloned_git_dir_path,
                os.path.join(repo_path, ""),
                verbose=verbose)

            commit_message_prefix = ""  # new commit from

        else:

            print("- repo does not exist ❌")

            # build repo path
            repo_path = challenge.path

            print("- init the git repository")

            # create git repo
            rc, output, error = git_init(repo_path, verbose=verbose)

            if rc != 0:

                print(Fore.RED
                      + "\nUnable to init git repo for challenge 🥺"
                      + Style.RESET_ALL
                      + f"\n- return code: {rc}"
                      + f"\n- output: {output}"
                      + f"\n- error: {error}")

                exit(1)

            # create repo if it does not exist
            if overwrite_sha is None or not overwrite_sha_repo_exists:

                print("- create gh repo")

                # create gh repo
                created_repo = gh_api_repo_create(
                    challenge.github_nickname,
                    challenge.repo_name,
                    token=gh_token)

                if created_repo is None:

                    print(Fore.RED
                          + "\nUnable to create gh repo for challenge 🤕"
                          + Style.RESET_ALL)

                    exit(1)

            print("- add remote")

            # build remote url
            repo_url = github_url(
                challenge.challenge_output,
                username=gh_nickname, token=gh_token)

            # add remote
            rc, output, error = git_remote_add(
                repo_path,
                DEFAULT_REMOTE_NAME,
                repo_url,
                verbose=verbose)

            if rc != 0:

                print(Fore.RED
                      + "\nUnable to add remote to git repo 🥺"
                      + Style.RESET_ALL
                      + f"\n- return code: {rc}"
                      + f"\n- output: {output}"
                      + f"\n- error: {error}")

                exit(1)

            commit_message_prefix = "myriad initial commit from "  # 🍇

        print("- add .gitignore")

        # build root gitignore path
        root_gitignore_path = os.path.join(
            ".",
            ".gitignore")

        # copy root gitignore to challenge
        cp(root_gitignore_path, repo_path, verbose=verbose)

        print("- add .syncignore and .challengifyignore")

        # iterate through ignore files
        for ignore_file in [".syncignore", ".challengifyignore"]:

            # check if file exists
            if not os.path.isfile(ignore_file):

                continue

            source_ignore_path = ignore_file

            # rename challengify ignore to avoid collisions
            if ignore_file == ".challengifyignore":

                ignore_file += "_myriad"

            destination_ignore_path = os.path.join(repo_path, ignore_file)

            # copy root ignore file to challenge
            cp(source_ignore_path, destination_ignore_path, verbose=verbose)

            # remove relative path from file content patterns
            rel_path = os.path.join(repo_path, "")
            rel_len = len(rel_path)

            with open(destination_ignore_path, "r") as file:

                # iterate through file rules
                content = [r[rel_len:] if r[:rel_len] == rel_path else r for r in file]

            # write updated file
            with open(destination_ignore_path, "w") as file:
                
                file.write("".join(content))

        print("- retrieve latest commit")

        # retrieve commit message
        if overwrite_sha is None:

            is_pull_request = event == GHA_EVENT_PULL_REQUEST

            # retrieve pr latest merged commit vs push latest commit
            latest_commit_message = get_latest_commit(
                latest_merged_commit=is_pull_request,
                verbose=verbose)

        else:

            # retrieve overwrite sha commit message
            latest_commit_message = get_latest_commit(
                commit_sha=overwrite_sha,
                verbose=verbose)

        print("- pre challengify add")

        # all the new files need to be referenced in git
        # in order to be visible by challengify
        rc, output, error = git_add(repo_path, verbose=verbose)

        if rc != 0:

            print(Fore.RED
                  + "\nUnable to add files to git 😬"
                  + Style.RESET_ALL
                  + f"\n- add return code: {rc}"
                  + f"\n- add output: {output}"
                  + f"\n- add error: {error}")

            exit(1)

        print("- challengify content")

        # build challengify target
        challengified_repo_path = os.path.join(
            os.path.dirname(repo_path),
            CHALLENGIFY_TARGET_PREFIX + os.path.basename(repo_path))

        # challengify the repository
        rc, output, error = challengify_service(
            path=repo_path,
            destination=challengified_repo_path,
            verbose=verbose)

        if rc != 0:

            print(Fore.RED
                  + "\nUnable to challengify individual challenge repo 😬"
                  + Style.RESET_ALL
                  + f"\n- challengify return code: {rc}"
                  + f"\n- challengify output: {output}"
                  + f"\n- challengify error: {error}")

            exit(1)

        print("- erase metadata")

        # build repo git dir path
        repo_git_dir_path = os.path.join(
            repo_path,
            ".git")

        # build challengified git dir path
        challengified_git_dir_path = os.path.join(
            challengified_repo_path,
            ".git")

        # move repo git dir to challengified dir
        mv(
            repo_git_dir_path,
            os.path.join(challengified_git_dir_path, ""),
            verbose=verbose)

        print("- create new commit")

        commit_message = commit_message_prefix + latest_commit_message

        # commit everything
        (rc, rc2), (output, output2), (error, error2) \
            = git_commit(
                challengified_repo_path,
                commit_message,
                verbose=verbose)
        ### PAVEL: no check for rc2
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

            exit(1)

        # Rename branch (will keep it master if it's already master)
        print("- renaming branch")
        rc, output, error = rename_branch(challengified_repo_path, base_ref)

        if rc != 0:

            print(Fore.RED
                  + "\nError during renaming branch 🤯"
                  + Style.RESET_ALL
                  + f"\n- return code: {rc}"
                  + f"\n- output: {output}"
                  + f"\n- error: {error}")

            exit(1)

        print("- push code to gh repo")

        # push code
        rc, output, error = git_push(
            challengified_repo_path,
            base_ref,
            force=True,
            verbose=verbose)

        if rc != 0:

            print(Fore.RED
                  + "\nUnable to push individual repo code ☹️"
                  + Style.RESET_ALL
                  + f"\n- return code: {rc}"
                  + f"\n- output: {output}"
                  + f"\n- error: {error}")

            exit(1)

        print("- update gh repo")

        # update gh repo
        updated_repo = gh_api_repo_update(
            challenge.github_nickname,
            challenge.repo_name,
            token=gh_token)

        if updated_repo is None:

            print(Fore.RED
                  + "\nUnable to update gh repo for challenge 🤕"
                  + Style.RESET_ALL)

            exit(1)


def conf_gh_auth(git_user_name, git_user_email, gh_nickname, gh_token):

    # conf git username
    rc, output, error = git_config("user.name", git_user_name)

    if rc != 0:

        print(Fore.RED
              + "\nUnable to config git username 🤕"
              + Style.RESET_ALL
              + f"\n- return code: {rc}"
              + f"\n- output: {output}"
              + f"\n- error: {error}")

        exit(1)

    # conf git email
    rc, output, error = git_config("user.email", git_user_email)

    if rc != 0:

        print(Fore.RED
              + "\nUnable to config git email 🤕"
              + Style.RESET_ALL
              + f"\n- return code: {rc}"
              + f"\n- output: {output}"
              + f"\n- error: {error}")

        exit(1)

    # gh auth
    rc, output, error = gh_auth(gh_token)  # gh_nickname unused

    if rc != 0:

        print(Fore.RED
              + "\nUnable to auth to gh 🤕"
              + Style.RESET_ALL
              + f"\n- return code: {rc}"
              + f"\n- output: {output}"
              + f"\n- error: {error}")

        exit(1)
