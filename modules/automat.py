from modules.kasa import *
from modules.rad import Rad
from modules.tovar import Tovar


class Automat:
    def __init__(self, vyska=5, sirka=5):
        self.rady = [[None for j in range(sirka)] for i in range(vyska)]
        self.kasa = Kasa()

    def katalog(self):
        for i, riadok in enumerate(self.rady):
            for j, rad in enumerate(riadok):
                if rad is not None:
                    print(f"[{i},{j}] - {rad.tovar.meno} (${rad.cena:.2f})")

    def nastavRad(self, riadok, stlpec, meno, cena, pocet=0):
        if riadok < 0 or stlpec < 0 or riadok >= len(self.rady) or stlpec >= len(self.rady[riadok]):
            return False
        # co je akoze typ ?
        self.rady[riadok][stlpec] = Rad(pocet, cena, Tovar(meno, meno))
        return True


if __name__ == '__main__':
    automat = Automat(2, 3)
    print(automat.nastavRad(1, 1, "COKE", 1.5, 5))
