import os

import psycopg2
import psycopg2.extensions
import psycopg2.extras

import Data.auth as auth

from typing import List

from Data.models import (plesalec, plesna_sola, tekmovanje, prijava)


psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

DB_PORT = os.environ.get("POSTGRES_PORT", 5432) #povežemo se z bazo


class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=auth.db,
            host=auth.host,
            user=auth.user,
            password=auth.password,
            port=DB_PORT
        )

        self.cur = self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )

    def dobi_plesalce(self) -> List[plesalec]:
        self.cur.execute("""
            SELECT id_plesalca, ime, priimek, emso, datum_rojstva, spol, id_sole
            FROM plesalec
            ORDER BY priimek, ime
        """)

        plesalci = [plesalec.from_dict(t) for t in self.cur.fetchall()]

        return plesalci

    def dobi_plesalce_sole(self, id_sole: int) -> List[plesalec]: #seznam vseh plesalcev na neki soli
           self.cur.execute("""
           SELECT id_plesalca, ime, priimek, emso, datum_rojstva, spol, id_sole
           FROM plesalec
           WHERE id_sole = %s  
           ORDER BY priimek, ime
           """, (id_sole,))

           plesalci = [plesalec.from_dict(t) for t in self.cur.fetchall()]

           return plesalci

    def dodaj_plesalca(self, t: plesalec): #če za nekega plesalca še ni podatkov v aplikaciji, ga šola lahko doda
           self.cur.execute("""
           INSERT INTO plesalec (ime, priimek, emso, datum_rojstva, spol, id_sole)
           VALUES (%s, %s, %s, %s, %s, %s)
           """, (t.ime, t.priimek, t.emso, t.datum_rojstva, t.spol, t.id_sole))

           self.conn.commit()

    def dobi_plesalca(self, id_plesalca: int) -> plesalec:  #to potrebuje aplikacija ko preverja ali plesalec ustreza starostni skupini
            self.cur.execute("""
            SELECT id_plesalca, ime, priimek, emso, datum_rojstva, spol, id_sole
            FROM plesalec
            WHERE id_plesalca = %s
            """, (id_plesalca,))

            return plesalec.from_dict(self.cur.fetchone())

    def dobi_sole(self) -> List[plesna_sola]:
            self.cur.execute("""
                SELECT id, ime, naslov, kontakt
                FROM plesna_sola
                ORDER BY  ime
            """)
    
            sole = [plesna_sola.from_dict(t) for t in self.cur.fetchall()]
    
            return sole

    def dobi_tekmovanja(self) -> List[tekmovanje]:
                self.cur.execute("""
                    SELECT id_tekmovanja, ime, lokacija, datum_od, datum_do
                    FROM tekmovanje
                    ORDER BY  datum_od
                """)
        
                tekmovanja = [tekmovanje.from_dict(t) for t in self.cur.fetchall()]
        
                return tekmovanja

    def dodaj_tekmovanje(self, t: tekmovanje):
           self.cur.execute("""
           INSERT INTO tekmovanje (ime, lokacija, datum_od, datum_do)
           VALUES (%s, %s, %s, %s)
           """, (t.ime, t.lokacija, t.datum_od, t.datum_do))

           self.conn.commit()

    def dobi_tekmovanje(self, id_tekmovanja: int) -> tekmovanje: #to potrebuje aplikacija ko preverja ali plesalec ustreza starostni skupini
            self.cur.execute("""
            SELECT id_tekmovanja, ime, lokacija, datum_od, datum_do
            FROM tekmovanje
            WHERE id_tekmovanja = %s
            """, (id_tekmovanja,))

            return tekmovanje.from_dict(self.cur.fetchone())

    def dobi_prijave(self) -> List[prijava]:
                self.cur.execute("""
                    SELECT id_prijave, id_sole, id_plesalca, id_tekmovanja, kategorija, disciplina, starostna_skupina
                    FROM prijava
                    ORDER BY  id_prijave
                """)
        
                prijave = [prijava.from_dict(t) for t in self.cur.fetchall()]
        
                return prijave

    def dodaj_prijavo(self, t: prijava):
            self.cur.execute("""
            INSERT INTO prijava (id_sole, id_plesalca, id_tekmovanja, kategorija, disciplina, starostna_skupina)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (t.id_sole, t.id_plesalca, t.id_tekmovanja, t.kategorija, t.disciplina, t.starostna_skupina))

            self.conn.commit()