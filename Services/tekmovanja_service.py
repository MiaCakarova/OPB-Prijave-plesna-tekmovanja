from Data.repository import Repo
from Data.models import *
from typing import List


class TekmovanjaService:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo

    def dobi_tekmovanja(self) -> List[tekmovanje]:
        return self.repo.dobi_tekmovanja()