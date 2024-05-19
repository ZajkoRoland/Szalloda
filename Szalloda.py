from abc import ABC, abstractmethod
from datetime import datetime,timedelta
import random

class Szoba(ABC):
    def __init__(self, Szobaszam, ar):
        self.Szobaszam = Szobaszam
        self.ar = ar
        self.Foglalt_szobak = False


    @abstractmethod
    def F_ar(self,NapokSz):
        return self.ar * NapokSz

    @abstractmethod
    def Szoba_foglalas(self):
        pass

    @abstractmethod
    def Szoba_lemondas(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, Szobaszam, ar= 15500):
        super().__init__(Szobaszam, ar)


    def Szoba_foglalas(self):
        if not self.Foglalt_szobak:
            self.Foglalt_szobak = True

    def Szoba_lemondas(self):
        if self.Foglalt_szobak:
            self.Foglalt_szobak = False

    def F_ar(self,NapokSz):
        return super().F_ar(NapokSz)


class KetagyasSzoba(Szoba):
    def __init__(self, Szobaszam, ar= 20000):
        super().__init__(Szobaszam, ar)

    def Szoba_foglalas(self):
        if not self.Foglalt_szobak:
            self.Foglalt_szobak = True

    def Szoba_lemondas(self):
        if self.Foglalt_szobak:
            self.Foglalt_szobak = False

    def F_ar(self,NapokSz):
        return super().F_ar(NapokSz)
class Szalloda:
    def __init__(self, nev):
        self.szobak = []
        self.foglalasok = []
        self.nev = nev

    def Szoba_hozzaadd(self, Szoba):
        self.szobak.append(Szoba)
    def Szobaszam_foglalas(self, Szobaszam, DatumK, DatumV):
        if DatumV <= DatumK:
            return None, "A vég dátum nem lehet kissebb mint a kezdő dátum."
        if any(F.Szobaszam == Szobaszam and not (F.DatumK >= DatumV or F.DatumV <= DatumK) for F in self.foglalasok):
            return None, "A szoba már foglalt ebben az időszakban."
        if DatumK < datetime.now():
            return None, "A kezdő datum nem lehet múltbéli."
        for szoba in self.szobak:
            if szoba.Szobaszam == Szobaszam:
                Napok = (DatumV - DatumK).days + 1
                ar = szoba.F_ar(Napok)
                self.foglalasok.append(Foglalas(Szobaszam,DatumK,DatumV))
                return ar, "Foglalás sikeresen megtörtént, Foglalás ára: {} Ft".format(ar)

        return None, "A megadott szobaszám nem található."

    def Szobaszam_lemondas(self, Szobaszam, DatumK):
        #szobaszam értékét stringgé alakítjuk biztonság kedvéért
        Szobaszam= str(Szobaszam)
        for Szoba, foglalas in enumerate(self.foglalasok):
            if foglalas.Szobaszam == Szobaszam and foglalas.DatumK == DatumK:
                del self.foglalasok[Szoba]
                return True, "Foglalás lemondva."
        return False, "Nincs ilyen foglalás."

    def Foglalas_listazas(self):
        if not self.foglalasok:
            return "Nincsenek aktív foglalasok."
        return "\n".join( f"Szobaszám: {F.Szobaszam}, Kezdete: {F.DatumK.date()}, Vége: {F.DatumV.date()}" for F in self.foglalasok)
    def Foglalas_ar(self):
        return {Szoba.Szobaszam: Szoba.ar for Szoba in self.szobak}
class Foglalas:
    def __init__(self, Szobaszam, DatumK , DatumV):
        self.Szobaszam = Szobaszam
        self.DatumK = DatumK
        self.DatumV = DatumV
def Felhasznaloi_felulet(szalloda):
    while True:
        print("1 - Foglalás")
        print("2 - Foglalás lemondása")
        print("3 - Foglalások listázása")
        print("4 - Szobák listázása")
        print("5 - Kilépés")

        valasztas = input("Válasszon egy opciót: ")

        if valasztas == "1":
            Szobaszam = input("Add meg a szoba számát amit le szeretnél foglalni: ")
            DatumK = datetime.strptime(input("Adja meg a kezdő dátumot (YYYY-MM-DD): "), "%Y-%m-%d")
            DatumV = datetime.strptime(input("Adja meg a befejező dátumot (YYYY-MM-DD): "), "%Y-%m-%d")
            ar , adatok = szalloda.Szobaszam_foglalas(Szobaszam,DatumK,DatumV)
            print(adatok)
        elif valasztas == "2":
            Szobaszam = int(input("Adja meg a szobaszámot: "))
            DatumK = datetime.strptime(input("Adja meg a kezdő dátumot (YYYY-MM-DD): "), "%Y-%m-%d")
            sikerult, adatok = szalloda.Szobaszam_lemondas(Szobaszam, DatumK)
            print(adatok)
        elif valasztas == "3":
            print("Foglalások:\n",szalloda.Foglalas_listazas())
        elif valasztas == "4":
            print("Szoba árak:", szalloda.Foglalas_ar())
        elif valasztas == "5":
            break
szalloda = Szalloda("grand hotel")
szalloda.Szoba_hozzaadd(EgyagyasSzoba("101"))
szalloda.Szoba_hozzaadd(EgyagyasSzoba("102"))
szalloda.Szoba_hozzaadd(EgyagyasSzoba("103"))
szalloda.Szoba_hozzaadd(EgyagyasSzoba("104"))
szalloda.Szoba_hozzaadd(KetagyasSzoba("201"))
szalloda.Szoba_hozzaadd(KetagyasSzoba("202"))
szalloda.Szoba_hozzaadd(KetagyasSzoba("203"))
szalloda.Szoba_hozzaadd(KetagyasSzoba("204"))

for i in range(8):
    room_number = random.choice([room.Szobaszam for room in szalloda.szobak])
    start_date = datetime.strptime(f"2024-06-{i + 1:02}", "%Y-%m-%d")
    end_date = start_date + timedelta(days=6)
    ar, _ = szalloda.Szobaszam_foglalas(room_number, start_date, end_date)


Felhasznaloi_felulet(szalloda)
