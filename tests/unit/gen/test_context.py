
from pathlib import Path

from wagon_myriad.github.context import get_challenge_root


class TestContext():

    data_path = Path("tests").joinpath("data", "gen")

    def test_challenge_path(self):
        """
        test that the path of the challenge of any file is correctly retrieved
        by looking at the location of the `.lewagon/metadata.yml` metadata file
        """

        # Arrange
        files = self.data_path.glob("**/*")

        # Act
        challenges = [get_challenge_root(file) for file in files]

        # Assert
        control_challenges = {
            "tests/data/gen/00-Setup/01-Challenge",
            "tests/data/gen/00-Setup/Reboot-me",
            "tests/data/gen/01-Module/02-Unit/03-Challenge",
            "tests/data/gen/01-Module/02-Unit/Recap",
            "tests/data/gen/Some/Other/Directory/Structure",
            None,
        }

        assert control_challenges == set(challenges)

        # Cleanup
