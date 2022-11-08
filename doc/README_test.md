
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

- create local `tests/tmp/gha-solutions` repo
- add remote to `lewagon-test/gha-solutions`

## act : base repo

- add change to `gha-solutions` repo from `tests/integration/source/gha-solutions`
- 👆 move .git dir
- push to `lewagon-test/gha-solutions`
- 👆 requires token with workflow credential

## assert : base repo

- wait for `myriad` gha to run on `lewagon-test/gha-solutions`

- clone `lewagon-test/gha-challenge` repo locally to `tests/tmp/gha-challenge`
- control the content of the cloned repo according to `tests/integration/control/gha-challenge`

## act : pull request

- add change to `gha-solutions` repo from `tests/integration/source/gha-solutions-pr`
- 👆 move .git dir
- push to `lewagon-test/gha-solutions`

## assert : pull request

- wait for `myriad` gha to run on `lewagon-test/gha-solutions`

- pull from `lewagon-test/gha-challenge`
- control the content of the cloned repo according to `tests/integration/control/gha-challenge-pr`

## cleanup

- delete `lewagon-test/gha-solutions` repo
- delete `lewagon-test/gha-challenge` repo

- delete local `tests/tmp/gha-solutions` repo
- delete local `tests/tmp/gha-challenge` repo
