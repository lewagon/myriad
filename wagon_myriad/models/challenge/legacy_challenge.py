
from wagon_myriad.models.challenge.challenge import Challenge


class LegacyChallenge(Challenge):

    def __init__(self, path, name, optional, solution, rake):

        self.name = name
        self.optional = optional
        self.solution = solution
        self.rake = rake

        super().__init__(path)

    def __repr__(self):

        return (
            "#<LegacyChallenge "
            f"path={self.path} "
            f"name={self.name} "
            f"optional={self.optional} "
            f"solution={self.solution} "
            f"rake={self.rake} "
            f"@={id(self)}>")
