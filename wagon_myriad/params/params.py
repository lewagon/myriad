
# the source org defines whether the process runs in prod
QA_ORG = "lewagon-qa"
TEST_ORG = "lewagon-test"
PROD_ORG = "lewagon"

# option to force the generation of all challenges
BRANCH_VERBOSE = "--verbose"
BRANCH_MYRIAD_FORCE = "--myriad-force"
BRANCH_MYRIAD_OVERWRITE = "--myriad-overwrite-"

# legacy list of supported courses
COURSE_QA = "qa"
COURSE_DATA = "data"
COURSE_WEB = "fullstack"
COURSE_DATA_ANALYTICS = "data-analytics"

COURSE_LIST = [
    COURSE_QA,
    COURSE_DATA,
    COURSE_WEB,
    COURSE_DATA_ANALYTICS]

GHA_COURSE_CONVERSION = {
    f"{QA_ORG}/qa-solutions": COURSE_QA,
    f"{TEST_ORG}/data-solutions": COURSE_DATA,
    f"{TEST_ORG}/fullstack-solutions": COURSE_WEB,
    f"{TEST_ORG}/data-analytics-solutions": COURSE_DATA_ANALYTICS,
    f"{PROD_ORG}/data-solutions": COURSE_DATA,
    f"{PROD_ORG}/fullstack-solutions": COURSE_WEB,
    f"{PROD_ORG}/data-anlaytics-solutions": COURSE_DATA_ANALYTICS,}

# legacy org selection
COURSE_ORG = dict(
    data="lewagon-test",
    fullstack="lewagon-test")

QA_COURSE_ORG = dict(
    qa="lewagon-qa")

PROD_COURSE_ORG = dict(
    data="lewagon-data",
    fullstack="lewagon-web",
    "data-analytics"="lewagon-data-analytics")

# legacy process
GHA_META_REPOS = dict(
    qa=("lewagon", "data-meta"),  # invalid but unused
    data=("lewagon", "data-meta"),
    fullstack=("lewagon", "fullstack-meta"))

# git params
DEFAULT_REMOTE_NAME = "origin"
DEFAULT_BRANCH = "master"

# gha events
GHA_EVENT_PUSH = "push"
GHA_EVENT_PULL_REQUEST = "pull_request"
