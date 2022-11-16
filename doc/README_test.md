
# install

``` bash
brew install act
```

# prod

`lewagon-qa` org secrets:
- `GEMFURY_PULL_TOKEN`: in order to install wagon_common, challengify, myriad
- `GMANCHON_DEV_TOKEN`: in order to allow to pull non released versions of wagon_common, challengify, myriad
- `USERNAME`: required by the Myriad GHA
- `TOKEN`: required by the Myriad GHA
- `VERBOSE`: run the Myriad GHA in verbose mode

# test scenario

## prerequisites

`lewagon-data` org wide conf:
- `secrets.GEMFURY_PULL_TOKEN`: gemfury token
- `secrets.VERBOSE`: optional
- `secrets.USERNAME`: github nickname
- `secrets.TOKEN`: github personal access token with **repo** + **admin:org** + **workflow** scopes

## arrange

- delete `lewagon-qa/qa-solutions` repo if exists
- delete `lewagon-qa/qa-challenge` repo if exists

- create git repo in `tests/data/myriad_gha/source/qa-solutions`
- add remote to `lewagon-qa/qa-solutions`

## act : base repo

- push to `lewagon-qa/qa-solutions`
- 👆 requires action using token with workflow credential

## assert : base repo

- wait for `myriad` gha to run on `lewagon-qa/qa-solutions`
- ping created repo using gh api

- clone `lewagon-qa/qa-challenge` repo locally to `tests/tmp/qa-challenge`
- control the content of the cloned repo according to `tests/data/myriad_gha/control/qa-challenge`

## act : pull request

- add change to `qa-solutions` repo from `tests/data/myriad_gha/source/qa-solutions-pr`
- 👆 move .git dir
- push to `lewagon-qa/qa-solutions`

## assert : pull request

- wait for `myriad` gha to run on `lewagon-qa/qa-solutions`
- ping created repo using gh api - wait for second commit

- pull from `lewagon-qa/qa-challenge`
- control the content of the cloned repo according to `tests/data/myriad_gha/control/qa-challenge-pr`

## cleanup

- delete `lewagon-qa/qa-solutions` repo
- delete `lewagon-qa/qa-challenge` repo

- delete local `tests/tmp/qa-solutions` repo
- delete local `tests/tmp/qa-challenge` repo
