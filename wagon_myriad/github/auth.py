
import os

from dotenv import load_dotenv, find_dotenv


def load_gh_auth():

    # load .env
    load_dotenv(find_dotenv())

    # retrieve token
    git_user_name = os.environ.get("GIT_USER_NAME")
    git_user_email = os.environ.get("GIT_USER_EMAIL")
    github_nickname = os.environ.get("GITHUB_NICKNAME")
    github_token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

    return git_user_name, git_user_email, github_nickname, github_token


def load_gh_token():

    # load .env
    load_dotenv(find_dotenv())

    # retrieve token
    github_token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

    return github_token
