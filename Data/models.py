from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import date, datetime

#Tukaj bomo definirali podatkovne modele, ki jih bomo uporabljali v aplikaciji.

#### Plesalec ####
@dataclass_json
@dataclass
class plesalec:
    id_plesalca: int = field(default=0)
    ime: str = field(default="")
    priimek: str = field(default="")
    emso: str = field(default="")
    datum_rojstva: date = field(default=None)
    spol: str = field(default="") #'moški','ženski,'drugo'
    id_sole: int = field(default=0) #da se bomo navezovali na plesno šolo

#### Plesna šola ####
@dataclass_json
@dataclass
class plesna_sola:
    id: int = field(default=0)
    ime: str = field(default="")
    naslov: str = field(default="")
    kontakt: str = field(default="") #lahko dajo tel ali mail

#### Tekmovanje ####
@dataclass_json
@dataclass
class tekmovanje:
    id_tekmovanja: int = field(default=0)
    ime: str = field(default="")
    lokacija: str = field(default="")
    datum_od: date = field(default=None)
    datum_do: date = field(default=None) #če tekmovanje traja en dan bo to polje prazno

#### Prijava ####
@dataclass_json
@dataclass
class prijava: 
    id_prijave: int = field(default=0)
    id_sole: int = field(default=0)
    id_plesalca: int = field(default=0)
    id_tekmovanja:int = field(default=0)
    kategorija: str = field(default="")
    disciplina: str = field(default="")
    starostna_skupina: str = field(default="")


