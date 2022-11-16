
# install

``` bash
brew install act
```

# test scenario

## prerequisites

`lewagon-data` org wide conf:
- `secrets.GEMFURY_PULL_TOKEN`: gemfury token
- `secrets.VERBOSE`: optional
- `secrets.USERNAME`: github nickname
- `secrets.TOKEN`: github personal access token with **repo** + **admin:org** + **workflow** scopes

## arrange

- delete `le-wagon-qa/gha-solutions` repo if exists
- delete `le-wagon-qa/gha-challenge` repo if exists

- create git repo in `tests/data/myriad_gha/source/gha-solutions`
- add remote to `le-wagon-qa/gha-solutions`

## act : base repo

- push to `le-wagon-qa/gha-solutions`
- 👆 requires action using token with workflow credential

## assert : base repo

- wait for `myriad` gha to run on `le-wagon-qa/gha-solutions`
- ping created repo using gh api

- clone `le-wagon-qa/gha-challenge` repo locally to `tests/tmp/gha-challenge`
- control the content of the cloned repo according to `tests/data/myriad_gha/control/gha-challenge`

## act : pull request

- add change to `gha-solutions` repo from `tests/data/myriad_gha/source/gha-solutions-pr`
- 👆 move .git dir
- push to `le-wagon-qa/gha-solutions`

## assert : pull request

- wait for `myriad` gha to run on `le-wagon-qa/gha-solutions`
- ping created repo using gh api - wait for second commit

- pull from `le-wagon-qa/gha-challenge`
- control the content of the cloned repo according to `tests/data/myriad_gha/control/gha-challenge-pr`

## cleanup

- delete `le-wagon-qa/gha-solutions` repo
- delete `le-wagon-qa/gha-challenge` repo

- delete local `tests/tmp/gha-solutions` repo
- delete local `tests/tmp/gha-challenge` repo
