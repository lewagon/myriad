
import os

from wagon_common.helpers.subprocess import run_command


def challengify_service(path, destination, verbose=False):
    """
    challengify the challenge at provided path
    """

    # build relative destination path
    destination_path = os.path.join(
        "..", os.path.basename(destination))

    # challengify
    command = [
        "challengify",
        "run",
        ".",
        "--force",            # the repo is going to contain the diffs from the commit
        "--ignore-cwd",       # ignore path from repo root to challenge
        "--destination",
        destination_path,
        ] + (["--verbose"] if verbose else [])

    rc, output, error = run_command(
        command,
        cwd=path,
        verbose=verbose)

    if verbose:
        print(output.decode("utf-8"))

    return rc, output, error


if __name__ == '__main__':

    test_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..", "..",
        "data-solutions",
        "07-Data-Engineering", "04-Predict-in-production", "01-FastAPI")

    rc, output, error = challengify_service(test_path)
    # print(rc, output, error)
