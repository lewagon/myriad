
import os
import yaml

from colorama import Fore, Style


class YamlFile:
    """
    load and save meta file data
    """

    def __init__(self, path, metadata=None):

        self.path = path

        self.metadata = metadata

    def save(self, content):

        # write file
        with open(self.path, "w") as file:
            yaml.dump(content, file, default_flow_style=False)

    def load(self):

        if not os.path.isfile(self.path):

            print(Fore.RED
                  + "\nMissing yaml file 🤒"
                  + Style.RESET_ALL
                  + f"\nfile path: {self.path}")

            raise FileNotFoundError(f"Missing yaml file: {self.path}")

        # load existing conf
        with open(self.path, "r") as file:
            content = yaml.load(file, Loader=yaml.FullLoader)

        # check content
        if not isinstance(content, dict):

            print(Fore.RED
                  + "\n\nInvalid content in solution meta file 🤒"
                  + "\nDictionary expected at root level"
                  + Style.RESET_ALL
                  + f"\n- meta file: {self.path}")

            raise ValueError(f"Invalid file content: {self.path}")

        return content
