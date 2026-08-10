import requests
from bs4 import BeautifulSoup
from datetime import date

URL = "https://www.plesna-zveza.si/dogodki?year=2026"
leto = 2026

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

dogodki = soup.find("div", class_="events-listing")

meseci = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "maj": 5, "jun": 6, "jul": 7, "avg": 8, "sep": 9, "okt": 10, "nov": 11, "dec": 12} #da bomo lahko zapisali kot datum

for dogodek in dogodki.find_all("li", class_="event-item"):

    #datum od
    od_dan = int(dogodek.find("span", class_="date").get_text(strip=True))
    od_mesec1 = dogodek.find("span", class_="month").get_text(strip=True)
    od_mesec = meseci[od_mesec1]
    od_datum = date(leto, od_mesec, od_dan)

    #ime dogodka
    ime = dogodek.find("div", class_="event-detail").find("a").get_text(strip=True)

    #lokacija in datum do (vidimo v html da sta združena)
    koda = dogodek.find("span", class_= "event-dayntime").get_text(" ", strip=True)

    do_datum = None #če traja tekmovanje samo en dan potem to polje ostane prazno in je zabeležen samo začetek
    lokacija = koda

    if koda.startswith("do"): #tako prepoznamo ali traja več dni
        razdeli = koda.split(";", 1)

        do_kdaj = razdeli[0] #najprej shranimo podatke o koncu ker so zapisani v obliki "do 17. okt"
        do_kdaj = do_kdaj.replace("do", "").strip()
        do_dan1, do_mesec1 = do_kdaj.split()

        do_dan = int(do_dan1.rstrip("."))
        do_mesec = meseci[do_mesec1]

        do_datum = date(leto, do_mesec, do_dan)

        lokacija = razdeli[1].strip()

    print("Ime:", ime)
    print("Od:", od_datum)
    print("Do:", do_datum)
    print("Lokacija:", lokacija)
    print("----------------------")

