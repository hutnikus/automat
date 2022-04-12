from modules.cashregister import *
from modules.row import Row
import json


class Automat:
    def __init__(self, height=5, width=5):
        self.items = [[None for j in range(width)] for i in range(height)]
        self.cashRegister = CashRegister()

    def __eq__(self, other):
        return self.items == other.items and self.cashRegister == other.cashRegister

    def getCatalog(self):
        retString = ""
        for i, col in enumerate(self.items):
            for j, row in enumerate(col):
                if isinstance(row, Row):
                    retString += f"[{i},{j}] - {row.goods} (${row.price:.2f})\n"
        return retString

    def _checkRowColInBounds(self, row, col):
        return 0 <= row < len(self.items) and 0 <= col < len(self.items[row])

    def setRow(self, rowNumber: int, colNumber: int, goodsName: str, price: float, quantity: int = 0):
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

    def getRow(self, rowNumber: int, colNumber: int):
        if not self._checkRowColInBounds(rowNumber, colNumber):
            raise IndexError()
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
        data = self.getData()
        with open(filename, "w") as file:
            json.dump(data, file)

    def load(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            self.loadFromData(data)


if __name__ == '__main__':
    automat = Automat(2, 3)
    print(automat.setRow(1, 1, "COKE", 1.5, 5))
    print(automat.getCatalog())
