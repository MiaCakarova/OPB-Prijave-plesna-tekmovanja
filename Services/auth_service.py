from Data.repository import Repo
from Data.models import *
import bcrypt
from typing import Union


class AuthService:
    repo: Repo

    def __init__(self):
        self.repo = Repo()


    def obstaja_uporabnik(self, uporabnik: str) -> bool: #preverimo a ze obstaja uporabnik s tem imenom
        sola = self.repo.dobi_solo_ui(uporabnik)

        return sola is not None


    def prijavi_uporabnika(self, uporabnik: str, geslo: str) -> Union[plesna_sola, bool]:  #preverimo ali sta uporabnisko ime in geslo pravilna
        sola = self.repo.dobi_solo_ui(uporabnik)
        if sola is None:
            return False
        
        geslo_bytes = geslo.encode('utf-8')

        succ = bcrypt.checkpw(geslo_bytes, sola.password_hash.encode('utf-8')) #ustvarimo hash

        if succ:
            return sola

        return False


    def dobi_uporabnika(self, uporabnik: str) -> plesna_sola:

        return self.repo.dobi_solo_ui(uporabnik)


    def dodaj_uporabnika(self, ime: str, naslov: str, kontakt: str, uporabnik: str, geslo: str) -> bool:

        if self.obstaja_uporabnik(uporabnik):
            return False

        geslo_bytes = geslo.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(geslo_bytes, salt)

        nova_sola = plesna_sola(
            ime=ime,
            naslov=naslov,
            kontakt=kontakt,
            uporabnisko_ime=uporabnik,
            password_hash=password_hash.decode())

        self.repo.dodaj_solo(nova_sola)

        return True