
class Lecture:

    def __init__(self, path, name, public):

        self.path = path
        self.name = name
        self.public = public

    def __repr__(self):

        return (
            "#<Lecture "
            f"path={self.path} "
            f"name={self.name} "
            f"public={self.public} "
            f"@={id(self)}>")
