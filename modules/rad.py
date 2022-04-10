from dataclasses import dataclass
from decimal import Decimal
from modules.tovar import *


class Rad:
    def __init__(self, pocet: int, cena: Decimal, tovar: str):
        self.pocet = pocet
        if cena <= 0:
            raise ValueError("Cena musí byť vyššia ako 0!")
        self.cena = round(cena, 2)
        if tovar =='' or tovar is None:
            raise ValueError("Tovar musí mať platné meno!")
        self.tovar = tovar

    def __str__(self):
        return f"{self.tovar}: {self.pocet}x {self.cena}"

    def __eq__(self, other):
        return (
            self.pocet == other.pocet and
            self.cena == other.cena and
            self.tovar == other.tovar
        )

    def getData(self):
        return {
            "pocet": self.pocet,
            "cena": str(self.cena),
            "tovar": self.tovar
        }

    def loadFromData(self, data):
        self.pocet = data["pocet"]
        self.cena = Decimal(data["cena"])
        self.tovar = data["tovar"]

    @staticmethod
    def createFromData(data):
        return Rad(
            data["pocet"],
            Decimal(data["cena"]),
            data["tovar"]
        )


if __name__ == '__main__':
    rad = Rad(1,Decimal(5.459),"keksik")
    print(rad)
    print(round(Decimal(5.65416),3).__repr__())