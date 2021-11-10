
from wagon_myriad.models.challenge.challenge import Challenge


class DotChallenge(Challenge):

    def __init__(self, path, metadata):

        self.metadata = metadata

        self.challenge_output = metadata.get("challenge_output")

        self.github_nickname = self.challenge_output.split("/")[-2]
        self.repo_name = self.challenge_output.split("/")[-1]

        super().__init__(path)

    def __repr__(self):

        return (
            "#<DotChallenge "
            f"path={self.path} "
            f"challenge_output={self.challenge_output} "
            f"@={id(self)}>")
