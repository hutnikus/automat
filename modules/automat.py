from modules.kasa import *
from modules.rad import Rad
import json


class Automat:
    def __init__(self, vyska=5, sirka=5):
        self.rady = [[None for j in range(sirka)] for i in range(vyska)]
        self.kasa = Kasa()

    def __eq__(self, other):
        return self.rady == other.rady and self.kasa == other.kasa

    def getKatalog(self):
        retString = ""
        for i, riadok in enumerate(self.rady):
            for j, rad in enumerate(riadok):
                if isinstance(rad, Rad):
                    retString += f"[{i},{j}] - {rad.tovar} (${rad.cena:.2f})\n"
        return retString

    def nastavRad(self, riadok: int, stlpec: int, meno: str, cena: float, pocet: int = 0):
        if riadok < 0 or stlpec < 0 or riadok >= len(self.rady) or stlpec >= len(self.rady[riadok]):
            return False
        self.rady[riadok][stlpec] = Rad(pocet, Decimal(cena), meno)
        return True

    def getData(self):
        def dataOrNone(data):
            if data is None:
                return None
            return data.getData()

        return {
            'rady': [[dataOrNone(data) for data in r] for r in self.rady],
            'kasa': self.kasa.getData()
        }

    def loadFromData(self, data):
        self.kasa.loadFromData(data["kasa"])
        self.rady = [[Rad.createFromData(rad) for rad in riadok] for riadok in data["rady"]]

    def save(self, filename):
        data = self.getData()
        with open(filename, "w") as file:
            json.dump(data, file)

    def load(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            self.loadFromData(data)


if __name__ == '__main__':
    automat = Automat(2, 3)
    print(automat.nastavRad(1, 1, "COKE", 1.5, 5))
    print(automat.getData())
