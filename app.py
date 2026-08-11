from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.plesalci_service import PlesalciService 
from Data.repository import Repo

import os

repo = Repo()
plesalci_service = PlesalciService(repo)

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', False)

@get('/')
def index():
    """
    Prvi osnutek domače strani
    """
    return template('domov.html')

@get('/plesalci')
def plesalci():
    """
    Stran 'Moji plesalci'. Aplikacija bo dobila id od šole, ki se prijavi.
    """
    seznam_plesalcev = plesalci_service.dobi_plesalce_sole(1)

    return template("plesalci.html", plesalci = seznam_plesalcev)

@get('/dodaj_plesalca')
def dodaj_plesalca():
    """
    Tukaj bo šola lahko dodala novega plesalca.
    """
    return template('dodaj_plesalca.html')

@get('/tekmovanja')
def tekmovanja():
    return "Stran Tekmovanja bo dodana kmalu."

@get('/prijave')
def prijave():
    return "Stran Moje prijave bo dodana kmalu."


if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)