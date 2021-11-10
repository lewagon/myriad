
# install

🚨 `wagon_common` and `challengify` are required as a dependency but are not yet published to PyPI and need to be manually installed first

``` bash
pip install git+ssh://git@github.com/lewagon/python-utilities.git
pip install git+ssh://git@github.com/lewagon/challengify.git
pip install git+ssh://git@github.com/lewagon/myriad.git
```

# uninstall

``` bash
pip uninstall -y myriad
pip uninstall -y challengify
pip uninstall -y wagon_common
```

# aliases

``` bash
alias myr="myriad $@"
```

# setup

copy `.env.sample` to `.env` and provide a valid gh personal token with repo read access

🚨 the command assumes that the following repos live in the same directory:
- utils
- data-meta
- data-solutions
- fullstack-meta
- fullstack-solutions

# usage

## challenge generation

``` bash
myr gen                       # generate the data-myriad directory of individual repos
myr gen -c fullstack          # generate fullstack-myriad
```

``` bash
myr unicity                   # sanity check for dot syllabus challenges gh repo names unicity
myr unicity -p                # list gh repo names along with challenge path

myr synchronized              # sanity check between meta syllabus, dot syllabus and look alike syllabus

myr ver                       # sanity check between conf and myriad repos
```

## meta repo

``` bash
myr list                      # list the content of the data syllabus
myr list -c fullstack         # list the content of the web syllabus

myr meta                      # generate meta directories and default files in individual solutions
myr meta -c fullstack         # generate meta directories for web syllabus
                              # add `.lewagon/metadata.yml` containing `challenge_output: lewagon-web/ruby-stupid-coaching`
                              # does not override `challenge_output` if it exists
                              # sanity check verifies the unicity of the gh repo names

myr meta --force              # overwrite web repo names with values from CHALLENGE_RENAMING

myr stub                      # generate program syllabus from data meta for the student clone tool
```

## syllabus exploration

``` bash
python -m wagon_myriad.exploration.syllabus_parser          # parse data syllabus
python -m wagon_myriad.exploration.verify_challenges        # verify data challenges
```

## tests

individual tests:

``` bash
python -m wagon_myriad.github.context                       # list challenges impacted by commits in current branch in ../../data-solutions vs origin/master
python -m wagon_myriad.models.syllabus.cloned_syllabus      # cloned meta repo syllabus loader
python -m wagon_myriad.models.syllabus.dot_syllabus         # dot syllabus loader
python -m wagon_myriad.models.syllabus.look_alike_syllabus  # look alike syllabus loader

python ../wagon_common/wagon_common/helpers/gh/url.py       # github repo helper
```

# gha

pr on branch name containing `--verbose` will output additional process info
pr on branch name containing `--myriad-force` will force the generation of all the challenges
pr on branch name containing `--myriad-overwrite-a7db5e4` will overwrite the individual repo history with initial commit from a7db5e4

the overwrite option will fail if the commit goes back in history to a point where a challenge path as determined in the HEAD by the `.lewagon` metadata is no longer valid

commits created with user name `github-actions` and email `github-actions@github.com`

# supported challenge patterns

- `01-Staff/01-Steff/01-Stiff/some/content/there.md`
- `01-Staff/01-Steff/Optional-Stiff/some/content/there.md`
- `01-Staff/01-Steff/Recap/some/content/there.md`
- `01-Staff/01-Steff/some/content/there.md`

# goal

create a sync process for individual challenges from data-solutions to individual myriad repositories

- have a library of independant challenge repositories of solutions (that are used by challengify to generate student readable solutions and challenges)
- the challenge repositories correspond to a version of a challenge
- the challenge repositories are indexed by modules of a program
- the program modules index the challenge repositories by branch as currently, which allows to create test programs for a batch for the evolutions of the challenges or lectures
- a challenge version evolves when its composition changes enough that it impacts the performance of the students
