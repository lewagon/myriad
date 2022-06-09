
## setup

### setup your `.env`

- Create a `.env` file from the `.env.sample`
- Create a [GitHub token](https://github.com/settings/tokens) (**Generate new token**) with the **repo** and **admin:org** scopes
- Save the token in the `GITHUB_PERSONAL_ACCESS_TOKEN` key of the `.env`
- Fill the rest of the `.env`

### directory structure

Setup the repository structure:

``` bash
.
├── challengify
├── data-challenges
├── data-meta
├── data-solutions
├── fullstack-challenges
├── fullstack-meta
├── fullstack-solutions
├── myriad
└── python-utilities          # wagon_common
```

Install the packages in editable mode (the `myriad` script will be running the cloned code):

``` bash
cd ~/code/lewagon/challengify && pip install -e .
cd ~/code/lewagon/myriad && pip install -e .
cd ~/code/lewagon/python-utilities && pip install -e .
```

## info

You should be able to run a few commands:

``` bash
cd ~/code/lewagon/data-solutions
myriad --help                 # list sub commands
myriad unicity -p             # list challenges and checks for unicity
myriad list                   # output parsed syllabus
```

## tests

### generate myriads

Generate myriads for commited content regarding to `master` (or any other sha):

``` bash
cd ~/code/lewagon/data-solutions
myriad gen -o lewagon-test -m master
```
