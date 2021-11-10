
import re

from wagon_myriad.params.params import (
    BRANCH_MYRIAD_OVERWRITE)


def extract_overwrite_sha(branch_name):

    assert(BRANCH_MYRIAD_OVERWRITE == "--myriad-overwrite-")

    # extract suffix
    re_pattern = r".*\-\-myriad-overwrite\-([^\-]*)"
    compiled_re = re.compile(re_pattern)
    matches = compiled_re.match(branch_name)

    # check matches
    if matches is not None:
        return matches[1]

    return None


if __name__ == '__main__':

    print(extract_overwrite_sha("some-stuff--myriad-force-other-stuff--myriad-overwrite-ad4cddd"))
    print(extract_overwrite_sha("some-stuff--myriad-force-other-stuff--myriad-overwrite-ad4cddd-anything"))
