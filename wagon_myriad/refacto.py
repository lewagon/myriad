
from colorama import Fore, Style


def build_sanity_check(challenges):
    """
    build unicity structure from dot syllabus challenges
    """

    # build repo names collection
    gh_repo_names = {}

    # iterate through challenges
    for challenge in challenges:

        # append set
        repo_challenges = gh_repo_names.get(challenge.challenge_output, [])
        repo_challenges.append(challenge)
        gh_repo_names[challenge.challenge_output] = repo_challenges

    return gh_repo_names


def sanity_check_report(gh_repo_names, challenges):

    # sanity check
    unique_repo_name_count = len(gh_repo_names.keys())

    if len(challenges) == unique_repo_name_count:

        print(Fore.GREEN
              + "\nSanity check: gh repo names are unique 🎉"
              + Style.RESET_ALL
              + f"\n- challenges: {len(challenges)}"
              + f"\n- unique gh repo names: {unique_repo_name_count}")

        return True

    print(Fore.RED
          + "\nSanity check: gh repo names are not unique ❌"
          + Style.RESET_ALL
          + f"\n- challenges: {len(challenges)}"
          + f"\n- unique gh repo names: {unique_repo_name_count}")

    # build duplicate list
    duplicate_names = {k: v for k, v in gh_repo_names.items() if len(v) > 1}

    print(Fore.RED
          + "\nNon unique gh repo names:"
          + Style.RESET_ALL)

    # show duplicates
    for repo_name, repo_challenges in duplicate_names.items():

        print(Fore.BLUE
              + f"- {repo_name}:"
              + Style.RESET_ALL)

        for repo_challenge in repo_challenges:

            print(f"  - {repo_challenge.path}"
                  + Style.RESET_ALL)

    return False


def meta_repo_syllabus_sanity_check(syllabus, list_path):

    # build sanity check
    gh_repo_names = build_sanity_check(syllabus.challenges)

    print(Fore.BLUE
          + "\nIndividual challenges:"
          + Style.RESET_ALL)

    # iterate through challenges
    for challenge in syllabus.challenges:

        if list_path:
            print(challenge.challenge_output, "-", challenge.path)
        else:
            print(challenge.challenge_output)

    # sanity check report
    sanity_check_ok = sanity_check_report(gh_repo_names, syllabus.challenges)

    if not sanity_check_ok:

        print(Fore.RED
              + "\nChallenges are not unique ❌"
              + Style.RESET_ALL)

        exit(1)
