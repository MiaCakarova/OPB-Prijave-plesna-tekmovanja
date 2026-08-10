from Data.repository import Repo
from Data.models import *
from typing import List

class PlesalciService:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo

    def dobi_plesalce_sole(self, id_sole: int) -> List[plesalec]:
        return self.repo.dobi_plesalce_sole(id_sole)

    def dodaj_plesalca(self, plesalec: plesalec):  #ko šola doda nekega plesalca, bo service preveril ali so vsi podatki izpolnjeni
        if plesalec.ime == "" or plesalec.priimek == "":
            raise ValueError("Ime in priimek sta obvezna.")
        if plesalec.datum_rojstva is None:
            raise ValueError("Datum rojstva je obvezen.")
        if plesalec.emso == "":
            raise ValueError("EMŠO je obvezen.")
        if plesalec.id_sole == 0:
            raise ValueError("error v aplikaciji")

        self.repo.dodaj_plesalca(plesalec)

