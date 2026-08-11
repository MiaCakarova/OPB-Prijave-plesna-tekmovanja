from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.plesalci_service import PlesalciService 
from Data.repository import Repo

import os

repo = Repo()
plesalci_service = PlesalciService(repo)

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

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


if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)