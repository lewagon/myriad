
from wagon_myriad.repositories.disk_repository import DiskRepository

from wagon_myriad.models.syllabus.dot_syllabus import DotSyllabus

from wagon_myriad.refacto import meta_repo_syllabus_sanity_check


class DotRepository(DiskRepository):

    def __init__(self, path: str):

        super().__init__(path)

        self.syllabus = DotSyllabus(path)

    def check_unicity(self, list_path):

        meta_repo_syllabus_sanity_check(self.syllabus, list_path)
