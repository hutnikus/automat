from decimal import Decimal
from typing import Union


class NotEnoughCoinsInRegisterException(Exception):
    pass


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
        return True

    def addChangeToBuffer(self, change: dict) -> bool:
        for coin in change:
            self.buffer[coin] += change[coin]
        return True

    def insertCoin(self, coin: str) -> bool:
        if coin not in self.coins:
            return False
        self.coins[coin] += 1
        return True

    @staticmethod
    def getCoinValue(coin: str) -> Union[Decimal, None, int]:
        valueDict = {
            "2e": 2.0,
            "1e": 1.0,
            "50c": 0.5,
            "20c": 0.2,
            "10c": 0.1,
            "5c": 0.05,
            "2c": 0.02,
            "1c": 0.01
        }
        if coin not in valueDict:
            return None
        return round(Decimal(valueDict[coin]), 2)

    def getDictSum(self, dict: dict) -> Decimal:
        sum = Decimal(0)
        for coin in dict:
            sum += dict[coin] * self.getCoinValue(coin)
        return sum

    def getBufferSum(self) -> Decimal:
        return self.getDictSum(self.buffer)

    def getCoinsSum(self) -> Decimal:
        return self.getDictSum(self.coins)

    def enoughCoinsInBuffer(self, amount: Decimal) -> bool:
        return self.getBufferSum() >= amount

    def calculateOverPayment(self, amount: Decimal) -> Decimal:
        return abs(amount - self.getBufferSum())

    def moveBufferToCoins(self):
        for coin in self.buffer:
            self.coins[coin] += self.buffer[coin]
            self.buffer[coin] = 0

    def getChange(self, amount: Decimal) -> dict:
        change = {}
        for coin in self.coins:
            while amount > 0 and self.coins[coin] > 0 and self.getCoinValue(coin) <= amount:
                change[coin] = change.get(coin, 0) + 1
                amount -= self.getCoinValue(coin)
                self.coins[coin] -= 1

        if amount > 0:
            # Not enough coins in the register
            for coin in change:
                numberOfCoins = change[coin]
                self.coins[coin] += numberOfCoins
                change[coin] = 0
                amount += self.getCoinValue(coin) * numberOfCoins
            raise NotEnoughCoinsInRegisterException(amount)
        return change

    def removeChangeFromCoins(self, change: dict):
        for coin in change:
            self.coins[coin] -= change[coin]

    def payCashGetChange(self, amount: Decimal) -> (dict, bool):
        # check if enough coins in buffer
        if not self.enoughCoinsInBuffer(amount):
            raise ValueError("Not enough coins in buffer")

        bufferCopy = self.buffer.copy()

        overPayment = self.calculateOverPayment(amount)

        # add buffer to coins and clear buffer
        self.moveBufferToCoins()

        # calculate change
        try:
            change = self.getChange(overPayment)
        except NotEnoughCoinsInRegisterException as e:
            # restore buffer
            self.buffer = bufferCopy
            # restore coins
            self.removeChangeFromCoins(bufferCopy)
            return bufferCopy, False

        return change, True

    def getTotalAccountValue(self) -> Decimal:
        return self.account + self.getCoinsSum()


