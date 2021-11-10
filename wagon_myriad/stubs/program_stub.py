
import os
import json
import yaml


def gen_program_stub(
        course, meta_syllabus, dot_syllabus, use_json=True):
    """
    Build kitt api program stub from challenges list
    This assumes all meta challenges are referenced in dot challenges
    """

    # build stub path
    stub_path = os.path.join(
        os.path.dirname(__file__),
        f"generated_{course}_program.{'json' if use_json else 'yml'}")

    # build program content
    challenges = meta_syllabus.challenges
    find_by_path = dot_syllabus.find_challenge_by_path

    content = [
        dict(path=c.path, repo=find_by_path(c.path)[0].challenge_output)
        for c in challenges]

    # save stub
    if use_json:

        with open(stub_path, "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)

    else:

        with open(stub_path, "w") as file:
            yaml.dump(content, file, default_flow_style=False)
