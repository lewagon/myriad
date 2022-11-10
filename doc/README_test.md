
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

- delete `Le-Wagon-QA/gha-solutions` repo if exists
- delete `Le-Wagon-QA/gha-challenge` repo if exists

- create git repo in `tests/data/myriad_gha/source/gha-solutions`
- add remote to `Le-Wagon-QA/gha-solutions`

## act : base repo

- push to `Le-Wagon-QA/gha-solutions`
- 👆 requires token with workflow credential

## assert : base repo

- wait for `myriad` gha to run on `Le-Wagon-QA/gha-solutions`
- ping created repo using gh api

- clone `Le-Wagon-QA/gha-challenge` repo locally to `tests/tmp/gha-challenge`
- control the content of the cloned repo according to `tests/data/myriad_gha/control/gha-challenge`

## act : pull request

- add change to `gha-solutions` repo from `tests/data/myriad_gha/source/gha-solutions-pr`
- 👆 move .git dir
- push to `Le-Wagon-QA/gha-solutions`

## assert : pull request

- wait for `myriad` gha to run on `Le-Wagon-QA/gha-solutions`
- ping created repo using gh api - wait for second commit

- pull from `Le-Wagon-QA/gha-challenge`
- control the content of the cloned repo according to `tests/data/myriad_gha/control/gha-challenge-pr`

## cleanup

- delete `Le-Wagon-QA/gha-solutions` repo
- delete `Le-Wagon-QA/gha-challenge` repo

- delete local `tests/tmp/gha-solutions` repo
- delete local `tests/tmp/gha-challenge` repo
