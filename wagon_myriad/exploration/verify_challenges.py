
import glob

import yaml
import requests

from wagon_myriad.github.auth import load_gh_token


# get syllabus
syllabus_url = "https://raw.githubusercontent.com/lewagon/data-meta/master/syllabus.yml"

# load gh pat
gh_pat = load_gh_token()

# build headers
headers = {
    "Authorization": f"token {gh_pat}"
}

response = requests.get(syllabus_url, headers=headers)

if response.status_code != 200:

    print("error getting syllabus")

    exit(-1)

# get default key
syllabus = yaml.safe_load(response.content)

default = syllabus.get("default", {})

# get days
days = default.get("days", {})

challenges = set([c["path"] for d in days.values() for c in d["exercises"]])

# list readmes
readmes = set([c[:-10] for c in glob.glob("**/README.md", recursive=True)])

# remove unsynced patterns
UNSYNCED_PATTERN = [
    "WIP",
    "HIDDEN",
    "ARCHIVE",
    "OLD",
    ]
EXCEPTION = "Threshold"
for pattern in UNSYNCED_PATTERN:
    readmes = set([r for r in readmes if pattern.lower() not in r.lower() or EXCEPTION.lower() in r.lower()])

print("\nsyllabus challenge directories without readmes:")
[print(f"- {c}") for c in sorted(challenges - readmes)]

# print("\nreadmes without syllabus challenges:")
# [print(f"- {c}") for c in sorted(readmes - challenges)]
