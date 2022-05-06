from modules.automat import Automat, EmptyError, NotEnoughMoneyError, NotEnoughChangeError
from enum import Enum


class Mode(Enum):
    USER = 0
    ADMIN = 1


class QueryType(Enum):
    COMMAND = 0
    SET_USER_MODE = 1
    ADD_ROW_CHOOSE_EMPTY = 2
    ADD_ROW_SET_NAME = 3
    ADD_ROW_SET_PRICE = 4
    REMOVE_ROW_CHOOSE_ROW = 5
    REMOVE_ROW_CONFIRM = 6
    CHANGE_ROW_PRICE = 7
    CHANGE_ROW_PRICE_NEW_PRICE = 8
    CHANGE_ROW_QUANTITY = 9
    CHANGE_ROW_QUANTITY_NEW_QUANTITY = 10
    BUY_ROW_CHOOSE_ROW = 11
    BUY_ROW_SELECT_PAYMENT = 12
    PAY_WITH_CASH_INSERT_COINS = 13
    CHANGE_REGISTER_SELECT_COIN = 14
    CHANGE_REGISTER_CHANGE_COIN = 15


class ResetError(Exception):
    pass


COIN_NUMBERS = {
    0: "2e",
    1: "1e",
    2: "50c",
    3: "20c",
    4: "10c",
    5: "5c",
    6: "2c",
    7: "1c"
}
COIN_VALUES = {
    "2e": "2.00€",
    "1e": "1.00€",
    "50c": "0.50€",
    "20c": "0.20€",
    "10c": "0.10€",
    "5c": "0.05€",
    "2c": "0.02€",
    "1c": "0.01€",
}


class Console:
    def __init__(self, automat: Automat, looping=True):
        self.automat = automat
        self.mode = Mode.ADMIN
        self.looping = looping
        self.currentQuery = QueryType.COMMAND
        self.stack = []
        self.startListenLoop()

    def startListenLoop(self):
        while self.looping:
            print(self.getCommandsList())
            command = input(self.getQueryText())
            try:
                if not self.executeCommand(command):
                    self.currentQuery = QueryType.COMMAND
            except ResetError:
                pass

    def getCurrentMode(self):
        if self.mode == Mode.USER:
            return "zákazník"
        elif self.mode == Mode.ADMIN:
            return "admin"
        return "¯\\_(ツ)_/¯"

    def getFullRowSelection(self):
        commands = ""
        for i, pos in enumerate(self.getGoods()[:-1].split("\n")):
            if i == 0:
                commands += f"{pos}\n"
                continue
            commands += f"{i - 1} - {pos}\n"
        return commands

    def getCommandsList(self):
        commands = "#" * 20 + "\n"
        commands += f"--mód {self.getCurrentMode()}--\n"

        if self.currentQuery != QueryType.COMMAND:
            commands += f"*** kedykoľvek sa môžte vrátiť do menu cez tlačidlo enter ***\n\n"

        if self.currentQuery == QueryType.COMMAND:
            commands += "0 - nastav mód\n"
            commands += "1 - zobraz stav tovarov\n"
            commands += "2 - nákup tovaru\n"

            if self.mode == Mode.ADMIN:
                commands += "10 - pridaj rad\n"
                commands += "11 - odstráň rad\n"
                commands += "12 - zmeň cenu radu\n"
                commands += "13 - zmeň počet kusov\n"
                commands += "14 - management kasy\n"

        elif self.currentQuery == QueryType.SET_USER_MODE:
            commands += "0 - mód zákazník\n"
            commands += "1 - mód admin\n"

        elif self.currentQuery == QueryType.ADD_ROW_CHOOSE_EMPTY:
            commands += "VOĽNÉ POZÍCIE:\n"
            for i, pos in enumerate(self.getPositions("empty")):
                commands += f"{i} - {pos}\n"

        elif self.currentQuery == QueryType.REMOVE_ROW_CHOOSE_ROW:
            commands += self.getFullRowSelection()

        elif self.currentQuery == QueryType.REMOVE_ROW_CONFIRM:
            commands += "0 - Nie\n"
            commands += "1 - Áno, odstrániť rad.\n"

        elif self.currentQuery == QueryType.CHANGE_ROW_PRICE:
            commands += self.getFullRowSelection()

        elif self.currentQuery == QueryType.CHANGE_ROW_PRICE_NEW_PRICE:
            item = self.automat.getRow(*self.stack[-1])
            commands += f"Pôvodná cena: {item.price}€\n"

        elif self.currentQuery == QueryType.CHANGE_ROW_QUANTITY:
            commands += self.getFullRowSelection()

        elif self.currentQuery == QueryType.CHANGE_ROW_QUANTITY_NEW_QUANTITY:
            item = self.automat.getRow(*self.stack[-1])
            commands += f"Pôvodné množstvo radu {item.goods}: {item.quantity}\n"

        elif self.currentQuery == QueryType.BUY_ROW_CHOOSE_ROW:
            commands += self.getFullRowSelection()

        elif self.currentQuery == QueryType.BUY_ROW_SELECT_PAYMENT:
            commands += "0 - kartou\n"
            commands += "1 - hotovosť\n"

        elif self.currentQuery == QueryType.PAY_WITH_CASH_INSERT_COINS:
            commands += f"Momentálny stav peňazí v automate: {self.automat.cashRegister.getBufferSum()}€\n"
            for number in COIN_NUMBERS:
                commands += f"{number} - {COIN_VALUES[COIN_NUMBERS[number]]}\n"
            commands += "10 - PLATBA\n"

        elif self.currentQuery == QueryType.CHANGE_REGISTER_SELECT_COIN:
            commands += f"Momentálny stav peňazí v automate: {self.automat.cashRegister.getCoinsSum()}€\n"
            coins = self.automat.cashRegister.coins.copy()
            for number in COIN_NUMBERS:
                commands += f"{number} - {COIN_VALUES[COIN_NUMBERS[number]]} ({coins[COIN_NUMBERS[number]]}ks)\n"

        elif self.currentQuery == QueryType.CHANGE_REGISTER_CHANGE_COIN:
            selected = self.stack[-1]
            commands += f"Pôvodné množstvo: {self.automat.cashRegister.coins[selected]}ks\n"

        return commands[:-1]

    def getQueryText(self):
        if self.currentQuery == QueryType.COMMAND:
            return "Zadaj príkaz: "
        if self.currentQuery == QueryType.SET_USER_MODE:
            return "Mód: "
        if self.currentQuery == QueryType.ADD_ROW_CHOOSE_EMPTY:
            return "Pozícia: "
        if self.currentQuery == QueryType.ADD_ROW_SET_NAME:
            return "Zadaj meno tovaru: "
        if self.currentQuery == QueryType.ADD_ROW_SET_PRICE:
            return "Zadaj cenu tovaru: "
        if self.currentQuery == QueryType.REMOVE_ROW_CHOOSE_ROW:
            return "Zadaj pozíciu, ktorú chceš uvoľniť: "
        if self.currentQuery == QueryType.REMOVE_ROW_CONFIRM:
            return "Ozaj chcete odstrániť rad? "
        if self.currentQuery == QueryType.CHANGE_ROW_PRICE:
            return "Zadaj pozíciu, ktorej chceš zmeniť cenu: "
        if self.currentQuery == QueryType.CHANGE_ROW_PRICE_NEW_PRICE:
            return "Zadaj novú cenu: "
        if self.currentQuery == QueryType.CHANGE_ROW_QUANTITY:
            return "Zadaj pozíciu, ktorej chceš zmeniť množstvo: "
        if self.currentQuery == QueryType.CHANGE_ROW_QUANTITY_NEW_QUANTITY:
            return "Zadaj nové množstvo: "
        if self.currentQuery == QueryType.BUY_ROW_CHOOSE_ROW:
            return "Zadaj pozíciu tovaru, ktorý chceš kupiť: "
        if self.currentQuery == QueryType.BUY_ROW_SELECT_PAYMENT:
            return "Zadaj spôsob platby: "
        if self.currentQuery == QueryType.PAY_WITH_CASH_INSERT_COINS:
            return "Vložte mincu: "
        if self.currentQuery == QueryType.CHANGE_REGISTER_SELECT_COIN:
            return "Vyberte mincu, ktorej chcete zmeniť množstvo: "
        if self.currentQuery == QueryType.CHANGE_REGISTER_CHANGE_COIN:
            return "Zadajte nové množstvo: "

        return ""

    def executeCommand(self, command: str) -> bool:
        words = command.split()
        if not words or words[0] == "":
            self.cancelAction()

        if self.currentQuery == QueryType.COMMAND:
            return self.handleTypeCommand(words)
        if self.currentQuery == QueryType.SET_USER_MODE:
            return self.setMode(words)
        if self.currentQuery == QueryType.ADD_ROW_CHOOSE_EMPTY:
            return self.choosePositionToAddRow(words)
        if self.currentQuery == QueryType.ADD_ROW_SET_NAME:
            return self.addRowSetName(words)
        if self.currentQuery == QueryType.ADD_ROW_SET_PRICE:
            return self.addRowSetPrice(words)
        if self.currentQuery == QueryType.REMOVE_ROW_CHOOSE_ROW:
            return self.chooseRowToRemove(words)
        if self.currentQuery == QueryType.REMOVE_ROW_CONFIRM:
            return self.confirmRemoveRow(words)
        if self.currentQuery == QueryType.CHANGE_ROW_PRICE:
            return self.selectRowToChangePrice(words)
        if self.currentQuery == QueryType.CHANGE_ROW_PRICE_NEW_PRICE:
            return self.changePrice(words)
        if self.currentQuery == QueryType.CHANGE_ROW_QUANTITY:
            return self.selectRowToChangeQuantity(words)
        if self.currentQuery == QueryType.CHANGE_ROW_QUANTITY_NEW_QUANTITY:
            return self.changeQuantity(words)
        if self.currentQuery == QueryType.BUY_ROW_CHOOSE_ROW:
            return self.selectRowToBuy(words)
        if self.currentQuery == QueryType.BUY_ROW_SELECT_PAYMENT:
            return self.selectPayment(words)
        if self.currentQuery == QueryType.PAY_WITH_CASH_INSERT_COINS:
            return self.insertCoins(words)
        if self.currentQuery == QueryType.CHANGE_REGISTER_SELECT_COIN:
            return self.selectCoinToChange(words)
        if self.currentQuery == QueryType.CHANGE_REGISTER_CHANGE_COIN:
            return self.changeCoinAmount(words)

        return False

    def handleTypeCommand(self, words):
        if words[0] == "0":
            self.currentQuery = QueryType.SET_USER_MODE
            return True
        if words[0] == "1":
            print(self.getGoods())
            return True
        if words[0] == "2":
            self.currentQuery = QueryType.BUY_ROW_CHOOSE_ROW
            return True

        if self.mode == Mode.ADMIN:
            if words[0] == "10":
                return self.startAddingRows()
            if words[0] == "11":
                return self.startRemovingRows()
            if words[0] == "12":
                return self.startChangingRowPrice()
            if words[0] == "13":
                return self.startChangingRowQuantity()
            if words[0] == "14":
                return self.startChangingRegister()

    def setMode(self, words):
        if len(words) != 1:
            return False
        try:
            int(words[0])
        except ValueError:
            self.cancelAction()

        if int(words[0]) in (0, 1):
            self.mode = Mode(int(words[0]))
            self.currentQuery = QueryType.COMMAND
            return True

        self.cancelAction()

    def getGoods(self):
        retStr = f"Rozmer automatu | výška: {len(self.automat.items)}, šírka: {len(self.automat.items[0])}\n"
        catalog = self.automat.getCatalog()
        if catalog:
            retStr += catalog
        else:
            retStr += "Prázdny automat!"
        return retStr

    def getPositions(self, typeStr: str) -> list:
        retList = []
        for i in range(len(self.automat.items)):
            for j in range(len(self.automat.items[0])):
                if self.automat.items[i][j] is None and typeStr == "empty":
                    retList.append((i, j))
                elif self.automat.items[i][j] is not None and typeStr == "full":
                    retList.append((i, j))
        return retList

    def getFullPositions(self) -> list:
        retList = []
        for i in range(len(self.automat.items)):
            for j in range(len(self.automat.items[i])):
                if self.automat.items[i][j] is not None:
                    retList.append((i, j))
        return retList

    def startAddingRows(self):
        self.currentQuery = QueryType.ADD_ROW_CHOOSE_EMPTY
        return True

    def choosePositionToAddRow(self, words):
        return self.chooseFromRows(words, QueryType.ADD_ROW_SET_NAME, "empty")

    def cancelAction(self, printMsg=True):
        if printMsg:
            print()
            print("Akcia prerušená!")
        self.currentQuery = QueryType.COMMAND
        self.stack = []

        if self.automat.cashRegister.getBufferSum() > 0:
            print("Automat vracia mince:")
            vratene = self.automat.cashRegister.returnCoins()
            for minca in vratene:
                print(f"{minca.replace('e', '€')} {vratene[minca]}x")

        raise ResetError()

    def addRowSetName(self, words):
        if not words:
            return False
        self.stack.append(" ".join(words))
        self.currentQuery = QueryType.ADD_ROW_SET_PRICE
        return True

    def addRowSetPrice(self, words):
        try:
            if len(words) != 1:
                raise ValueError()

            volba = float(words[0])
            if volba <= 0:
                raise ValueError()
        except ValueError:
            print("Cena tovaru musí byť kladné číslo!")
            return True

        self.stack.append(volba)
        return self.finishAddingRow()

    def finishAddingRow(self):
        price = self.stack.pop()
        name = self.stack.pop()
        row, col = self.stack.pop()

        if not self.automat.addRow(row, col, name, price, 0):
            print("Niekde nastala chyba!")

        return False

    def startRemovingRows(self):
        self.currentQuery = QueryType.REMOVE_ROW_CHOOSE_ROW
        return True

    def chooseFromRows(self, words, nextQuery, positionType):
        try:
            if len(words) != 1:
                raise ValueError()

            volba = int(words[0])
            positions = self.getPositions(positionType)
            if volba not in range(len(positions)):
                raise ValueError()
        except ValueError:
            print("Nesprávne číslo!")
            return True

        self.stack.append(positions[volba])
        self.currentQuery = nextQuery
        return True

    def chooseRowToRemove(self, words):
        return self.chooseFromRows(words, QueryType.REMOVE_ROW_CONFIRM, "full")

    def confirmRemoveRow(self, words):
        if len(words) != 1:
            return False
        if words[0] == "1":
            return self.finishRemovingRow()
        if words[0] == "0":
            return self.startRemovingRows()
        return False

    def finishRemovingRow(self):
        row, col = self.stack.pop()
        if not self.automat.removeRow(row, col):
            print("Niekde nastala chyba!")
        return False

    def startChangingRowPrice(self):
        self.currentQuery = QueryType.CHANGE_ROW_PRICE
        return True

    def selectRowToChangePrice(self, words):
        return self.chooseFromRows(words, QueryType.CHANGE_ROW_PRICE_NEW_PRICE, "full")

    def changePrice(self, words):
        try:
            if len(words) != 1:
                raise ValueError()

            volba = float(words[0])
            if volba <= 0:
                raise ValueError()
        except ValueError:
            print("Cena tovaru musí byť kladné číslo!")
            return True

        self.stack.append(volba)
        return self.finishChangingPrice()

    def finishChangingPrice(self):
        price = self.stack.pop()
        row, col = self.stack.pop()
        self.automat.getRow(row, col).price = price
        return False

    def startChangingRowQuantity(self):
        self.currentQuery = QueryType.CHANGE_ROW_QUANTITY
        return True

    def selectRowToChangeQuantity(self, words):
        return self.chooseFromRows(words, QueryType.CHANGE_ROW_QUANTITY_NEW_QUANTITY, "full")

    def changeQuantity(self, words):
        try:
            if len(words) != 1:
                raise ValueError()

            volba = int(words[0])
            if volba < 0:
                raise ValueError()
        except ValueError:
            print("Množstvo tovaru musí byť kladné celé číslo!")
            return True

        self.stack.append(volba)
        return self.finishChangingQuantity()

    def finishChangingQuantity(self):
        quantity = self.stack.pop()
        row, col = self.stack.pop()
        self.automat.getRow(row, col).quantity = quantity
        return False

    def selectRowToBuy(self, words):
        return self.chooseFromRows(words, QueryType.BUY_ROW_SELECT_PAYMENT, "full")

    def selectPayment(self, words):
        if len(words) != 1:
            print("Nesprávna voľba!")
            return True

        choice = words[0].strip()

        if choice == "0":
            return self.payWithCard()
        if choice == "1":
            return self.payWithCash()

        print("Nesprávna voľba!")
        return True

    def payWithCard(self):
        row, col = self.stack.pop()

        if self.automat.buyItemWithCard(row, col):
            print("Zaplatené!")
            for _ in range(5):
                print(".")

            item = self.automat.getRow(row, col)
            print(f"Môžte si vybrať tovar {item.goods}. Platili ste {item.price}€.")
            return False

        print("Nepodarilo sa zaplatiť!")
        return True

    def payWithCash(self):
        self.currentQuery = QueryType.PAY_WITH_CASH_INSERT_COINS
        return True

    def insertCoins(self, words):
        try:
            if len(words) != 1:
                raise ValueError()

            volba = int(words[0])
            if volba not in [0, 1, 2, 3, 4, 5, 6, 7, 10]:
                raise ValueError()
        except ValueError:
            print("Nesprávna voľba!")
            return True

        if volba in COIN_NUMBERS:
            if not self.automat.cashRegister.insertCoin(COIN_NUMBERS[volba]):
                print("Nepodarilo sa vložiť mincu!")
                self.currentQuery = QueryType.PAY_WITH_CASH_INSERT_COINS
            return True

        if volba == 10:
            return self.finishCashPayment()

        print("Nesprávne číslo!")
        return True

    def finishCashPayment(self):
        row, col = self.stack.pop()

        changeBack = {}
        try:
            changeBack = self.automat.buyItemWithCash(row, col)
        except EmptyError:
            print("Zvolené miesto je prázdne!")
            return False
        except NotEnoughMoneyError:
            print("Nevložili ste dostatočné množstvo mincí!")
            self.stack.append((row, col))
            self.currentQuery = QueryType.PAY_WITH_CASH_INSERT_COINS
            return True
        except NotEnoughChangeError:
            print("Automat nemá mince na vydaj, skúste neskôr!")
            self.cancelAction()

        print("Zaplatené!")
        for _ in range(5):
            print(".")

        item = self.automat.getRow(row, col)
        print(f"Môžte si vybrať tovar {item.goods}. Platili ste {item.price}€.")
        self.automat.cashRegister.addChangeToBuffer(changeBack)
        print("Automat vracia mince:")
        vratene = self.automat.cashRegister.returnCoins()
        for minca in vratene:
            print(f"{minca.replace('e', '€')} {vratene[minca]}x")

        return False

    def startChangingRegister(self):
        self.currentQuery = QueryType.CHANGE_REGISTER_SELECT_COIN
        return True

    def selectCoinToChange(self, words):
        try:
            if len(words) != 1:
                raise ValueError()

            volba = int(words[0])
            if volba not in range(len(COIN_NUMBERS)):
                raise ValueError()
        except ValueError:
            print("Nesprávna voľba!")
            return True

        self.stack.append(COIN_NUMBERS[volba])
        self.currentQuery = QueryType.CHANGE_REGISTER_CHANGE_COIN
        return True

    def changeCoinAmount(self, words):
        try:
            if len(words) != 1:
                raise ValueError()

            volba = int(words[0])
            if volba < 0:
                raise ValueError()
        except ValueError:
            print("Hodnota musí byť kladné celé číslo alebo 0!")
            return True

        zadane = self.stack.pop()
        self.automat.cashRegister.coins[zadane] = int(volba)

        return self.startChangingRegister()
