from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.plesalci_service import PlesalciService 
from Services.tekmovanja_service import TekmovanjaService
from Services.prijave_service import PrijaveService
from Data.repository import Repo
from Data.models import plesalec
from Data.models import prijava
from datetime import date

from bottle import response

import os

repo = Repo()
plesalci_service = PlesalciService(repo)
tekmovanja_service = TekmovanjaService(repo)
prijave_service = PrijaveService(repo)

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

    response.content_type = 'text/html; charset=UTF-8'

    return template("plesalci.html", plesalci = seznam_plesalcev)

@get('/dodaj_plesalca')
def dodaj_plesalca():
    """
    Tukaj bo šola lahko dodala novega plesalca.
    """
    response.content_type = 'text/html; charset=UTF-8'
    return template('dodaj_plesalca.html')

@post('/dodaj_plesalca')
def dodaj_plesalca_post():

    ime = request.forms.getunicode('ime')
    priimek = request.forms.getunicode('priimek')
    emso = request.forms.getunicode('emso')
    datum_rojstva = request.forms.getunicode('datum_rojstva')
    spol = request.forms.getunicode('spol')

    nov_plesalec = plesalec(
        ime=ime,
        priimek=priimek,
        emso=emso,
        datum_rojstva=date.fromisoformat(datum_rojstva),
        spol=spol,
        id_sole=1
    )

    plesalci_service.dodaj_plesalca(nov_plesalec)

    redirect(url('/plesalci'))

@get('/tekmovanja')
def tekmovanja():
    seznam_tekmovanj = tekmovanja_service.dobi_tekmovanja()
    return template("tekmovanja.html", tekmovanja = seznam_tekmovanj)

@get('/prijave')
def prijave():
    seznam_prijav = prijave_service.dobi_prijave_dto(1)
    return template('prijave.html', prijave=seznam_prijav, sporocilo=None)

@get('/prijavi_plesalca/<id_tekmovanja:int>')
def prijavi_plesalca(id_tekmovanja):
    plesalci = plesalci_service.dobi_plesalce_sole(1)
    return template('prijavi_plesalca.html', plesalci=plesalci, id_tekmovanja=id_tekmovanja, napaka = None)

@post('/prijavi_plesalca')
def prijavi_plesalca_post():
    id_plesalca = int(request.forms.getunicode('id_plesalca'))
    id_tekmovanja = int(request.forms.getunicode('id_tekmovanja'))
    kategorija = request.forms.getunicode('kategorija')
    disciplina = request.forms.getunicode('disciplina')
    starostna_skupina = request.forms.getunicode('starostna_skupina')

    nova_prijava = prijava(id_sole=1, id_plesalca=id_plesalca, id_tekmovanja=id_tekmovanja, kategorija=kategorija, disciplina=disciplina, starostna_skupina=starostna_skupina)

    try:
        prijave_service.dodaj_prijavo(nova_prijava)
        seznam_prijav = prijave_service.dobi_prijave_dto(1)
        
        return template('prijave.html', prijave=seznam_prijav, sporocilo="Prijava je bila uspešna!")
    
    except ValueError as napaka:
        plesalci = plesalci_service.dobi_plesalce_sole(1)

        return template('prijavi_plesalca.html', plesalci=plesalci, id_tekmovanja=id_tekmovanja, napaka=str(napaka))





if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)