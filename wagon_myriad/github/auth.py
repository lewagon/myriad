
import os

from dotenv import load_dotenv, find_dotenv


def load_gh_auth():

    # load .env
    load_dotenv(find_dotenv())

    # retrieve token
    git_token = os.environ["GIT_PUSH_TOKEN"]
    gh_token = os.environ["GH_API_CREATE_TOKEN"]

    return git_token, gh_token


def load_gh_token():

    # load .env
    load_dotenv(find_dotenv())

    # retrieve token
    gh_token = os.environ["GH_API_CREATE_TOKEN"]

    return gh_token
