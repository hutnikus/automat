from modules.cashregister import *
from modules.row import Row
import json
from typing import Union, List
import os


class EmptyError(Exception):
    pass


class NotEnoughMoneyError(Exception):
    pass

class NotEnoughChangeError(Exception):
    pass


class Automat:
    def __init__(self, height: int = 5, width: int = 5):
        self.items: List[List[Union[None, Row]]] = [[None for _ in range(width)] for _ in range(height)]
        self.cashRegister = CashRegister()

    def __eq__(self, other):
        return self.items == other.items and self.cashRegister == other.cashRegister

    def getCatalog(self) -> str:
        retString = ""
        for i, col in enumerate(self.items):
            for j, row in enumerate(col):
                if isinstance(row, Row):
                    retString += f"[{i},{j}] - {row.goods} ({row.price:.2f}€) - {row.quantity}ks\n"
        return retString

    def _checkRowColInBounds(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.items) and 0 <= col < len(self.items[row])

    def setRow(self, rowNumber: int, colNumber: int, goodsName: str, price: float, quantity: int = 0) -> bool:
        if not self._checkRowColInBounds(rowNumber, colNumber):
            return False
        self.items[rowNumber][colNumber] = Row(quantity, Decimal(price), goodsName)
        return True

    def addRow(self, rowNumber: int, colNumber: int, goodsName: str, price: float, quantity: int = 0):
        if not self._checkRowColInBounds(rowNumber, colNumber):
            return False
        if self.items[rowNumber][colNumber] is not None:
            return False
        self.items[rowNumber][colNumber] = Row(quantity, Decimal(price), goodsName)
        return True

    def removeRow(self, rowNumber: int, colNumber: int):
        if not self._checkRowColInBounds(rowNumber, colNumber):
            return False
        if self.items[rowNumber][colNumber] is None:
            return False
        self.items[rowNumber][colNumber] = None
        return True

    def getRow(self, rowNumber: int, colNumber: int) -> Union[Row, None]:
        if not self._checkRowColInBounds(rowNumber, colNumber):
            raise IndexError("Riadok alebo stĺpec mimo limit!")
        return self.items[rowNumber][colNumber]

    def getData(self):
        def dataOrNone(data):
            if data is None:
                return None
            return data.getData()

        return {
            'items': [[dataOrNone(data) for data in r] for r in self.items],
            'cashRegister': self.cashRegister.getData()
        }

    def loadFromData(self, data):
        self.cashRegister.loadFromData(data["cashRegister"])
        self.items = [[Row.createFromData(row) for row in col] for col in data["items"]]

    def save(self, filename):
        rootDir = getRootDirectory()
        if not os.path.exists(os.path.join(rootDir, "files")):
            os.makedirs(os.path.join(rootDir, "files"))

        data = self.getData()
        with open(os.path.join(rootDir,"files",filename), "w") as file:
            json.dump(data, file)

    def load(self, filename):
        path = os.path.join(getRootDirectory(), "files", filename)

        if not os.path.exists(path):
            raise FileNotFoundError("Súbor neexistuje!")

        with open(path, "r") as file:
            data = json.load(file)
            self.loadFromData(data)

    def buyItemWithCard(self, row: int, col: int) -> bool:
        row = self.getRow(row, col)
        if not row:
            raise EmptyError("Zvolené miesto je prázdne")

        if row.quantity == 0:
            raise EmptyError("Zvolené miesto je prázdne")

        row.adjustQuantity(-1)
        self.cashRegister.addToAccount(row.price)

        return True

    def insertCoin(self, coin: str) -> bool:
        return self.cashRegister.insertCoin(coin)

    def buyItemWithCash(self, row: int, col: int) -> dict:
        row = self.getRow(row, col)
        if not row:
            raise EmptyError("Zvolené miesto je prázdne")

        if row.quantity == 0:
            raise EmptyError("Zvolené miesto je prázdne")

        if not self.cashRegister.enoughCoinsInBuffer(row.price):
            raise NotEnoughMoneyError("Nedostatok peňazí na zaplatenie")

        changeResult = self.cashRegister.payCashGetChange(row.price)

        if not changeResult[1]:
            raise NotEnoughChangeError("Nedostatok peňazí na vrátenie")

        row.adjustQuantity(-1)

        return changeResult[0]


def getRootDirectory():
    def recursiveFindParent(path):
        files = os.listdir(path)
        if "modules" in files:
            return path
        return recursiveFindParent(os.path.dirname(path))

    dirname = recursiveFindParent(os.path.dirname(__file__))
    return dirname

if __name__ == '__main__':
    automat = Automat(2, 3)
    print(automat.getCatalog())
