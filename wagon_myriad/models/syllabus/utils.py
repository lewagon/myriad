
from colorama import Fore, Style

from wagon_myriad.models.module import Module
from wagon_myriad.models.leaf import Leaf
from wagon_myriad.models.challenge.legacy_challenge import LegacyChallenge
from wagon_myriad.models.lecture import Lecture
from wagon_myriad.models.video import Video


def parse_syllabus(syllabus_content):
    """
    parse syllabus into module, leaf, challenge, lecture and video objects
    """

    # get default key
    default = syllabus_content.get("default", {})

    # load modules
    syllabus_modules = default.get("modules", {})

    modules = [
        Module(slug, c.get("name"), c.get("icon"), c.get("path"))
        for slug, c in syllabus_modules.items()]

    # load leafs
    days = default.get("days", {})

    leafs = []
    challenges = []
    lectures = []
    videos = []

    for _, content in days.items():

        # leaf attributes
        path = content.get("path")
        name = content.get("name")
        split = content.get("split")
        flashcards = content.get("flashcards", False)
        teacher_ratio = content.get("teacher_ratio", 1)

        # leaf module
        module_slug = content.get("module_slug")

        # attach leaf to module
        module = [m for m in modules if m.slug == module_slug]

        if len(module) > 0:
            module = module[0]
        else:
            module = None

        # leaf content
        exercises_content = content.get("exercises", [])
        lectures_content = content.get("lectures", [])
        videos_content = content.get("lecture", {})

        # add leaf
        leaf = Leaf(module, path, name, split, flashcards, teacher_ratio)

        if module is not None:
            module.attach(leaf)

        leafs.append(leaf)

        # load challenges
        for exercise_content in exercises_content:

            # challenge attributes
            path = exercise_content.get("path")
            name = exercise_content.get("name")
            optional = exercise_content.get("optional")
            solution = exercise_content.get("solution")
            rake = exercise_content.get("rake")

            # add challenge
            challenge = LegacyChallenge(path, name, optional, solution, rake)

            leaf.attach_challenge(challenge)

            challenges.append(challenge)

        # load lectures
        for lecture_content in lectures_content:

            path = lecture_content.get("path")
            name = lecture_content.get("name")
            public = lecture_content.get("public", False)

            lecture = Lecture(path, name, public)

            leaf.attach_lecture(lecture)

            lectures.append(lecture)

        # load videos
        for language, video_content in videos_content.items():

            video_id = video_content.get("video", "")

            video = Video(language, video_id)

            leaf.attach_video(video)

            videos.append(video)

    return modules, leafs, challenges, lectures, videos


def print_syllabus(syllabus):
    """
    print syllabus models
    """

    print(Fore.GREEN
          + "\nModules:"
          + Style.RESET_ALL)
    [print(e) for e in syllabus.modules]

    print(Fore.GREEN
          + "\nModule leafs:"
          + Style.RESET_ALL)
    for module in syllabus.modules:

        print(Fore.BLUE
              + f"\nModule: {module.name}"
              + Style.RESET_ALL)
        [print(e) for e in module.leafs]

    print(Fore.GREEN
          + "\nLeafs:"
          + Style.RESET_ALL)
    [print(e) for e in syllabus.leafs]

    print(Fore.GREEN
          + "\nLeaf content:"
          + Style.RESET_ALL)
    for leaf in syllabus.leafs:

        print(Fore.BLUE
              + f"\n🌱 Leaf: {leaf.name}"
              + Style.RESET_ALL
              + f"\nModule: {leaf.module.name}")

        print(Fore.BLUE
              + "\nChallenges"
              + Style.RESET_ALL)

        [print(e) for e in leaf.challenges]

        print(Fore.BLUE
              + "\nLectures"
              + Style.RESET_ALL)

        [print(e) for e in leaf.lectures]

        print(Fore.BLUE
              + "\nVideos"
              + Style.RESET_ALL)

        [print(e) for e in leaf.videos]

    print(Fore.GREEN
          + "\nChallenges:"
          + Style.RESET_ALL)
    [print(e) for e in syllabus.challenges]

    print(Fore.GREEN
          + "\nLectures:"
          + Style.RESET_ALL)
    [print(e) for e in syllabus.lectures]

    print(Fore.GREEN
          + "\nVideos:"
          + Style.RESET_ALL)
    [print(e) for e in syllabus.videos]
