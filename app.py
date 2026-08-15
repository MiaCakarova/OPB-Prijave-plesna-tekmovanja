from functools import wraps


from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.plesalci_service import PlesalciService 
from Services.tekmovanja_service import TekmovanjaService
from Services.prijave_service import PrijaveService
from Services.auth_service import AuthService
from Data.repository import Repo
from Data.models import plesalec
from Data.models import prijava as Prijava
from datetime import date

import os

repo = Repo()
plesalci_service = PlesalciService(repo)
tekmovanja_service = TekmovanjaService(repo)
prijave_service = PrijaveService(repo)
auth = AuthService()

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', False)

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")

        print("cookie uporabnik:", cookie)

        if cookie:
            return f(*args, **kwargs)
        return template("prijava.html", napaka="Potrebna je prijava!")
        
    return decorated

@get('/')
@cookie_required
def index():
    """
    Prvi osnutek domače strani
    """
    return template('domov.html')

#### Plesalci ####

@get('/plesalci')
@cookie_required
def plesalci():
    """
    Stran 'Moji plesalci'
    """
    id_sole = dobi_id_sole() #aplikacija zve kdo je trenutno prijavljen
    seznam_plesalcev = plesalci_service.dobi_plesalce_sole(id_sole) #dobimo samo plesalce te plesne šole, druge šole ne rabijo videti naših plesalcev

    response.content_type = 'text/html; charset=UTF-8'

    return template("plesalci.html", plesalci = seznam_plesalcev)

@get('/dodaj_plesalca')
@cookie_required
def dodaj_plesalca():
    """
    Tukaj bo šola lahko dodala novega plesalca.
    """
    response.content_type = 'text/html; charset=UTF-8'
    return template('dodaj_plesalca.html')

@post('/dodaj_plesalca')
@cookie_required
def dodaj_plesalca_post():

    ime = request.forms.getunicode('ime') #unicode zavzame tudi šumnike 
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
        id_sole=dobi_id_sole()
    )

    plesalci_service.dodaj_plesalca(nov_plesalec) #pošlje servicu da preveri a vse štima

    redirect(url('/plesalci')) #potem nas spet vrže na stran 'Moji plesalci', kjer lahko vidimo dodanega plesalca

#### Tekmovanja ####

@get('/tekmovanja')
@cookie_required
def tekmovanja():
    seznam_tekmovanj = tekmovanja_service.dobi_tekmovanja()
    return template("tekmovanja.html", tekmovanja = seznam_tekmovanj)

#### Prijave ####

@get('/prijave')
@cookie_required
def prijave():
    id_sole = dobi_id_sole()
    seznam_prijav = prijave_service.dobi_prijave_dto(id_sole)
    return template('prijave.html', prijave=seznam_prijav, sporocilo=None)

@get('/prijavi_plesalca/<id_tekmovanja:int>') #v url-ju se doda id tekmovanja
@cookie_required
def prijavi_plesalca(id_tekmovanja):
    id_sole = dobi_id_sole()
    plesalci = plesalci_service.dobi_plesalce_sole(id_sole)
    return template('prijavi_plesalca.html', plesalci=plesalci, id_tekmovanja=id_tekmovanja, napaka = None)

@post('/prijavi_plesalca')
@cookie_required
def prijavi_plesalca_post():
    id_plesalca = int(request.forms.getunicode('id_plesalca'))
    id_tekmovanja = int(request.forms.getunicode('id_tekmovanja'))
    kategorija = request.forms.getunicode('kategorija')
    disciplina = request.forms.getunicode('disciplina')
    starostna_skupina = request.forms.getunicode('starostna_skupina')

    nova_prijava = Prijava(
        id_sole=dobi_id_sole(),
        id_plesalca=id_plesalca, 
        id_tekmovanja=id_tekmovanja, 
        kategorija=kategorija, 
        disciplina=disciplina, 
        starostna_skupina=starostna_skupina)

    try:
        prijave_service.dodaj_prijavo(nova_prijava)
        seznam_prijav = prijave_service.dobi_prijave_dto(dobi_id_sole())
        
        return template('prijave.html', prijave=seznam_prijav, sporocilo="Prijava je bila uspešna!")
    
    except ValueError as napaka:
        plesalci = plesalci_service.dobi_plesalce_sole(dobi_id_sole())

        return template('prijavi_plesalca.html', plesalci=plesalci, id_tekmovanja=id_tekmovanja, napaka=str(napaka))

#### Prijava/odjava/registracija uporabnika ####

@get('/prijava')
def prijava():
    return template('prijava.html', napaka=None)

@post('/prijava')
def prijava_post():

    uporabnik = request.forms.getunicode('uporabnik')
    geslo = request.forms.getunicode('geslo')

    if not auth.obstaja_uporabnik(uporabnik):
        return template('prijava.html', napaka="Uporabnik s tem uporabniškim imenom ne obstaja.")

    sola = auth.prijavi_uporabnika(uporabnik, geslo)

    if sola:
        response.set_cookie("uporabnik", uporabnik)
        response.set_cookie("id_sole", str(sola.id))

        redirect(url('/'))

    return template('prijava.html', napaka="Napaka! Napačno geslo ali uporabniško ime.")

@get('/odjava')
def odjava():

    print("cookie pred odjavo:", request.get_cookie("uporabnik"))

    response.delete_cookie("uporabnik")
    response.delete_cookie("id_sole")

    return template('prijava.html', napaka=None)

@get('/registracija')
def registracija():
    return template('registracija.html', napaka=None)

@post('/registracija')
def registracija_post():
    ime = request.forms.getunicode('ime')
    naslov = request.forms.getunicode('naslov')
    kontakt = request.forms.getunicode('kontakt')
    uporabnik = request.forms.getunicode('uporabnik')
    geslo = request.forms.getunicode('geslo')

    if any(znak in uporabnik.lower() for znak in ['č', 'š', 'ž']):
        return template('registracija.html', napaka="Uporabniško ime ne sme vsebovati znakov 'č', 'š', 'ž'.")

    uspeh = auth.dodaj_uporabnika(ime, naslov, kontakt, uporabnik, geslo)

    if not uspeh:
        return template('registracija.html', napaka="Uporabniško ime že obstaja.")

    return template('prijava.html', napaka=None, sporocilo = "Po registraciji je potrebna prijava.")

def dobi_id_sole():
    return int(request.get_cookie("id_sole"))

if __name__ == "__main__":
   
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)