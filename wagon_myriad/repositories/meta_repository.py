
from wagon_myriad.repositories.disk_repository import DiskRepository

from wagon_myriad.models.syllabus.cloned_syllabus import ClonedSyllabus
from wagon_myriad.models.syllabus.utils import print_syllabus

from wagon_common.helpers.gh.url import GitHubRepo


class MetaRepository(DiskRepository):

    def __init__(self, path: str, repo: GitHubRepo):

        self.repo = repo

        super().__init__(path)

        self.syllabus = ClonedSyllabus(path)

    def print_syllabus(self):

        print_syllabus(self.syllabus)
