
class Leaf:

    def __init__(self, module, path, name, split, flashcards, teacher_ratio):

        self.module = module

        self.path = path
        self.name = name
        self.split = split
        self.flashcards = flashcards
        self.teacher_ratio = teacher_ratio

        self.challenges = []
        self.lectures = []
        self.videos = []

    def __repr__(self):

        return (
            "#<Leaf "
            f"path={self.path} "
            f"name={self.name} "
            f"split={self.split} "
            f"flashcards={self.flashcards} "
            f"teacher_ratio={self.teacher_ratio} "
            f"@={id(self)}>")

    def attach_challenge(self, challenge):

        self.challenges.append(challenge)

    def attach_lecture(self, lecture):

        self.lectures.append(lecture)

    def attach_video(self, video):

        self.videos.append(video)
