from decimal import Decimal


class Kasa:
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
        self.mince = {
            "2e": 0,
            "1e": 0,
            "50c": 0,
            "20c": 0,
            "10c": 0,
            "5c": 0,
            "2c": 0,
            "1c": 0
        }
        self.ucet = Decimal(0)

    def getData(self):
        return {
            "buffer": self.buffer,
            "mince": self.mince,
            "ucet": str(self.ucet)
        }

    def loadFromData(self, data):
        self.buffer = data["buffer"],
        self.mince = data["mince"],
        self.ucet = Decimal(data["ucet"])