
## setup

### setup your `.env`

- Create a `.env` file from the `.env.sample`
- Create a [GitHub token](https://github.com/settings/tokens) (**Generate new token**) with the **repo** and **admin:org** scopes
- Save the token in the `GITHUB_PERSONAL_ACCESS_TOKEN` key of the `.env`
- Fill the rest of the `.env`

### directory structure

⚠️ We recommand to create a dedicated root directory because myriad will:
- Clone myriad repositories at the same level as the solutions repository
- Add `.git` repositories to all challenges having synchronized content within the solutions repository

Setup the repository structure:

``` bash
.                                       # ~
└── code
    └── lewagon-myriad
        ├── challengify
        ├── data-challenges
        ├── data-meta
        ├── data-solutions
        ├── fullstack-challenges
        ├── fullstack-meta
        ├── fullstack-solutions
        ├── myriad
        └── python-utilities            # wagon_common
```

Install the packages in editable mode (the `myriad` script will be running the cloned code):

``` bash
# cd ~/code/lewagon-myriad/challengify && pip install -e .  # latest version not running with myriad at the moment
pip install challengify==0.3.1
cd ~/code/lewagon-myriad/myriad && pip install -e .
cd ~/code/lewagon-myriad/python-utilities && pip install -e .
```

## info

You should be able to run a few commands:

``` bash
cd ~/code/lewagon-myriad/data-solutions

myriad --help                 # list sub commands
myriad unicity -p             # list challenges and check for unicity
myriad list                   # output parsed syllabus
```

## generate myriads

⚠️ Generate myriads 🚨 IN THE **TEST** ORGANISATION 🚨 please 🙏

Requirements:
- Add commits (branch does not matter) to the content
- Reference the last known commit sha in the `-m` param (here `master`)

``` bash
cd ~/code/lewagon-myriad/data-solutions

myriad gen -o lewagon-test -m master

myriad gen -o lewagon-test -m master -v  # verbose mode

# myriad gen --gha -c lewagon-test/data-solutions -m master
```
