import os

import psycopg2
import psycopg2.extensions
import psycopg2.extras

import Data.auth as auth


psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

DB_PORT = os.environ.get("POSTGRES_PORT", 5432)


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

    def dobi_plesalce(self):
        self.cur.execute("""
            SELECT id_plesalca, ime, priimek, emso, datum_rojstva, spol, id_sole
            FROM plesalec
            ORDER BY priimek, ime
        """)

        return self.cur.fetchall()