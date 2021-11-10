
class Syllabus:

    def __init__(self):

        self.modules = None
        self.leafs = None
        self.challenges = None
        self.lectures = None
        self.videos = None

        self.load_syllabus()

    def load_syllabus(self):

        raise NotImplementedError

    def find_challenge_by_path(self, path):

        return [c for c in self.challenges if c.path == path]
