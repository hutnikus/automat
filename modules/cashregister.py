from decimal import Decimal


class CashRegister:
    def __init__(self):
        self.buffer = {
            "2e": 0,
            "1e": 0,
            "50c": 0,
            "20c": 0,
            "10c": 0,
            "5c": 0,
            "2c": 0,
            "1c": 0
        }
        self.coins = {
            "2e": 0,
            "1e": 0,
            "50c": 0,
            "20c": 0,
            "10c": 0,
            "5c": 0,
            "2c": 0,
            "1c": 0
        }
        self.account = round(Decimal(0), 2)

    def __eq__(self, other):
        return self.buffer == other.buffer and self.coins == other.coins and self.account == other.account

    def getData(self):
        return {
            "buffer": self.buffer,
            "coins": self.coins,
            "account": str(self.account)
        }

    def loadFromData(self, data):
        self.buffer = data["buffer"]
        self.coins = data["coins"]
        self.account = Decimal(data["account"])

    def addToAccount(self, amount: Decimal) -> bool:
        if amount <= 0:
            return False
        self.account = round(self.account+amount, 2)
