
from collections.abc import Mapping

import yaml
import requests

from colorama import Fore, Style

from wagon_myriad.github.auth import load_gh_token


# load gh pat
gh_pat = load_gh_token()

# build headers
headers = {
    "Authorization": f"token {gh_pat}"
}

# get syllabus
syllabus_url = "https://raw.githubusercontent.com/lewagon/data-meta/master/syllabus.yml"

response = requests.get(syllabus_url, headers=headers)

if response.status_code != 200:

    print("error getting syllabus")

    exit(-1)

# get default key
syllabus = yaml.safe_load(response.content)

default = syllabus.get("default", {})

# get lecture path
print(Fore.BLUE
      + "\nLecture path template"
      + Style.RESET_ALL)

lecture_path_template = default.get("lecture_path_template", {})

print(Fore.GREEN
      + "\nlecture path template:"
      + Style.RESET_ALL
      + f"\n- {lecture_path_template}")

# get modules
print(Fore.BLUE
      + "\nModules"
      + Style.RESET_ALL)

modules = default.get("modules", {})

for module, module_content in modules.items():

    module_name = module_content.get("name", "")
    module_icon = module_content.get("icon", "")
    module_path = module_content.get("path", "")

    print(Fore.GREEN
          + f"\nmodule {module}:"
          + Style.RESET_ALL
          + f"\n- {lecture_path_template}"
          + f"\n- name {module_name}"
          + f"\n- icon {module_icon}"
          + f"\n- path {module_path}")

# get submodules
submodules = default.get("submodules", [])

print(Fore.BLUE
      + "\nSubmodules"
      + Style.RESET_ALL
      + "".join([f"\n- {s}" for s in submodules]))

# get days
print(Fore.BLUE
      + "\nDays"
      + Style.RESET_ALL)

days = default.get("days", {})

exercises_keys = set()

for day, content in days.items():

    module_slug = content.get("module_slug", "")
    submodule = content.get("submodule", "")
    path = content.get("path", "")
    name = content.get("name", "")
    flashcards = content.get("flashcards", False)
    exercises = content.get("exercises", "")
    lectures = content.get("lectures", "")
    videos = content.get("lecture", "")
    teacher_ratio = content.get("teacher_ratio", 0)

    print(Fore.GREEN
          + f"\nday {day}:"
          + Style.RESET_ALL
          + f"\n- slug {module_slug}"
          + f"\n- submodule {submodule}"
          + f"\n- path {path}"
          + f"\n- name {name}"
          + f"\n- flashcards {flashcards}"
          + f"\n- exercises {exercises}"
          + f"\n- lectures {lectures}"
          + f"\n- lecture {videos}"
          + f"\n- teacher_ratio {teacher_ratio}")

    assert type(module_slug) == str
    assert type(submodule) == str
    assert type(path) == str
    assert type(name) == str
    assert type(flashcards) == bool
    assert type(exercises) == list
    assert type(lectures) == list or lectures == ""
    assert isinstance(videos, Mapping) or videos == ""
    assert type(teacher_ratio) == int

    # exercises
    for exercise_index, exercise in enumerate(exercises):
        exercise_path = exercise.get("path", "")
        exercise_name = exercise.get("name", "")
        exercise_optional = exercise.get("optional", "")
        exercise_solution = exercise.get("solution", "")
        exercise_rake = exercise.get("rake", "")

        exercises_keys.update(exercise.keys())

        print(Fore.BLUE
              + f"\n    exercise {exercise_index}:"
              + Style.RESET_ALL
              + f"\n    - path {exercise_path}"
              + f"\n    - name {exercise_name}"
              + f"\n    - optional {exercise_optional}"
              + f"\n    - solution {exercise_solution}"
              + f"\n    - rake {exercise_rake}")

    # lectures
    for lecture_index, lecture in enumerate(lectures):
        lecture_path = lecture.get("path", "")
        lecture_name = lecture.get("name", "")
        lecture_public = lecture.get("public", False)

        print(Fore.BLUE
              + f"\n    lecture {lecture_index}:"
              + Style.RESET_ALL
              + f"\n    - path {lecture_path}"
              + f"\n    - name {lecture_name}"
              + f"\n    - public {lecture_public}")

    # videos
    if videos != "":

        for language, video in videos.items():

            video_id = video.get("video", "")

            print(Fore.BLUE
                  + f"\n    language {language}:"
                  + Style.RESET_ALL
                  + f"\n    - id {video_id}")

print(Fore.BLUE
      + "\nExercise keys:"
      + Style.RESET_ALL
      + "".join([f"\n- {k}" for k in exercises_keys]))
