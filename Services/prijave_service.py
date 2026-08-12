from Data.repository import Repo
from Data.models import *
from typing import List


class PrijaveService:
    def __init__(self, repo: Repo):
        self.repo = repo

    def dodaj_prijavo(self, prijava: prijava):
        if prijava.id_plesalca == "":
            raise ValueError("Plesalec mora biti izbran.")

        if prijava.id_tekmovanja == "":
            raise ValueError("Tekmovanje mora biti izbrano.")

        if prijava.kategorija == "":
            raise ValueError("Kategorija je obvezna.")

        if prijava.disciplina == "":
            raise ValueError("Disciplina je obvezna.")

        if prijava.starostna_skupina == "":
            raise ValueError("Starostna skupina je obvezna.")

        self.preveri_starostno_skupino(prijava)
        self.repo.dodaj_prijavo(prijava)
        

    def preveri_starostno_skupino(self, prijava: prijava): #to bo dalo opozorilo, če plesalca pomotoma zabeležijo k napačni starostni skupini
        plesalec = self.repo.dobi_plesalca(prijava.id_plesalca)
        tekmovanje = self.repo.dobi_tekmovanje(prijava.id_tekmovanja)
        starost = tekmovanje.datum_od.year - plesalec.datum_rojstva.year

        if prijava.starostna_skupina == "otroci":
            ustreza = starost <= 12

        elif prijava.starostna_skupina == "mladinci":
            ustreza = 13 <= starost <= 16

        elif prijava.starostna_skupina == "člani":
            ustreza = 17 <= starost <= 30

        elif prijava.starostna_skupina == "člani 2":
            ustreza = starost >= 31

        else:
            raise ValueError("Neveljavna starostna skupina.")

        if not ustreza:
            raise ValueError(
                f"Plesalec ne ustreza izbrani starostni skupini. "
            )