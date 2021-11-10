
import os

from colorama import Fore, Style


class DiskRepository:

    def __init__(self, path: str):

        self.path = path

        if not os.path.isdir(self.path):

            print(Fore.RED
                  + "\nMissing repo directory 🤒"
                  + Style.RESET_ALL
                  + f"\nrepo path: {self.path}")

            raise FileNotFoundError(f"Missing repo directory: {self.path}")
