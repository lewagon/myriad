
# the source org defines whether the process runs in prod
QA_ORG = "lewagon-qa"
TEST_ORG = "lewagon-test"
PROD_ORG = "lewagon"

# option to force the generation of all challenges
BRANCH_VERBOSE = "--verbose"
BRANCH_MYRIAD_FORCE = "--myriad-force"
BRANCH_MYRIAD_OVERWRITE = "--myriad-overwrite-"

# legacy list of supported courses
COURSE_DATA = "data"
COURSE_WEB = "fullstack"

COURSE_LIST = [
    COURSE_DATA,
    COURSE_WEB]

GHA_COURSE_CONVERSION = {
    f"{QA_ORG}/gha-solutions": COURSE_DATA,
    f"{TEST_ORG}/data-solutions": COURSE_DATA,
    f"{TEST_ORG}/fullstack-solutions": COURSE_WEB,
    f"{PROD_ORG}/data-solutions": COURSE_DATA,
    f"{PROD_ORG}/fullstack-solutions": COURSE_WEB}

# legacy org selection
COURSE_ORG = dict(
    data="lewagon-test",
    fullstack="lewagon-test")

PROD_COURSE_ORG = dict(
    data="lewagon-data",
    fullstack="lewagon-web")

# legacy process
GHA_META_REPOS = dict(
    data=("lewagon", "data-meta"),
    fullstack=("lewagon", "fullstack-meta"))

# git params
DEFAULT_REMOTE_NAME = "origin"
DEFAULT_BRANCH = "master"

# gha events
GHA_EVENT_PUSH = "push"
GHA_EVENT_PULL_REQUEST = "pull_request"
