from modules.kasa import *


class Automat:
    def __init__(self, vyska=5, sirka=5):
        self.rady = [[None for j in range(sirka)] for i in range(vyska)]
        self.kasa = Kasa()


if __name__ == '__main__':
    automat = Automat(2, 3)
