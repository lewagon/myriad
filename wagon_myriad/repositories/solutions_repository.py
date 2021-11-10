
from wagon_myriad.repositories.disk_repository import DiskRepository


class SolutionsRepository(DiskRepository):

    def __init__(self, path: str):

        super().__init__(path)
