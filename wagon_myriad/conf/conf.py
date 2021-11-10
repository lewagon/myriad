
import os
import yaml

from colorama import Fore, Style


def get_conf_path(meta_repo):
    """
    get gh sync conf path
    """

    # build conf path
    conf_path = os.path.join(
        meta_repo,
        "gh_sync.yml")

    return conf_path


def load_gh_sync_conf(meta_repo):
    """
    read course gh sync yaml file
    """

    # retrieve conf path
    conf_path = get_conf_path(meta_repo)

    # check if file exists
    if not os.path.isfile(conf_path):

        print(Fore.RED
              + "\nGH sync conf file does not exist"
              + Style.RESET_ALL
              + f"\n- conf file: {conf_path}")

        # return an empty conf
        return {}

    else:

        print(Fore.GREEN
              + "\nLoad gh sync conf file"
              + Style.RESET_ALL
              + f"\n- conf file: {conf_path}")

    # load conf
    with open(conf_path, "r") as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)

    return conf


def save_gh_sync_conf(meta_repo, data):
    """
    save course gh sync yaml file
    """

    # retrieve conf path
    conf_path = get_conf_path(meta_repo)

    print(Fore.GREEN
          + "\nSave gh sync conf file"
          + Style.RESET_ALL
          + f"\n- conf file: {conf_path}")

    # save conf
    with open(conf_path, "w") as file:
        yaml.dump(data, file, default_flow_style=False)
