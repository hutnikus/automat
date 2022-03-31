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
