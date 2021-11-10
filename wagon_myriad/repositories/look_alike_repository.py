
from wagon_myriad.repositories.disk_repository import DiskRepository

from wagon_myriad.models.syllabus.look_alike_syllabus import LookAlikeSyllabus


class LookAlikeRepository(DiskRepository):

    def __init__(self, path: str):

        super().__init__(path)

        self.syllabus = LookAlikeSyllabus(path)
