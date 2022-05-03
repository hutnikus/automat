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


class ResetError(Exception):
    pass


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
        if self.currentQuery == QueryType.COMMAND:
            commands += "0 - nastav mód\n"
            commands += "1 - zobraz stav tovarov\n"
            commands += "2 - nákup tovaru\n"

            if self.mode == Mode.ADMIN:
                commands += "10 - pridaj rad\n"
                commands += "11 - odstráň rad\n"
                commands += "12 - zmeň cenu radu\n"
                commands += "13 - zmeň počet kusov\n"
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
            commands += "0 - 2€\n"
            commands += "1 - 1€\n"
            commands += "2 - 0.50€\n"
            commands += "3 - 0.20€\n"
            commands += "4 - 0.10€\n"
            commands += "5 - 0.05€\n"
            commands += "6 - 0.02€\n"
            commands += "7 - 0.01€\n"
            commands += "10 - PLATBA\n"
            commands += "11 - ZRUŠIŤ\n"
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
            for j in range(len(self.automat.items[0])):
                if self.automat.items[i][j] is not None:
                    retList.append((i, j))
        return retList

    def startAddingRows(self):
        self.currentQuery = QueryType.ADD_ROW_CHOOSE_EMPTY
        return True

    def choosePositionToAddRow(self, words):
        if len(words) != 1:
            return False
        emptyPositions = self.getPositions("empty")
        try:
            int(words[0])
        except ValueError:
            self.cancelAction()

        if int(words[0]) in range(len(emptyPositions)):
            self.stack.append(emptyPositions[int(words[0])])
            self.currentQuery = QueryType.ADD_ROW_SET_NAME
            return True
        return False

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
                print(f"{minca.replace('e','€')} {vratene[minca]}x")

        raise ResetError()

    def addRowSetName(self, words):
        if not words:
            return False
        self.stack.append(" ".join(words))
        self.currentQuery = QueryType.ADD_ROW_SET_PRICE
        return True

    def addRowSetPrice(self, words):
        def isCorrectNumber(num):
            try:
                return float(num) > 0
            except ValueError:
                return False

        if len(words) != 1:
            return False

        if isCorrectNumber(words[0]):
            self.stack.append(float(words[0]))
            return self.finishAddingRow()

        print("Cena tovaru musí byť kladné číslo!")
        return True

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

    def chooseRowToRemove(self, words):
        if len(words) != 1:
            return False
        fullPositions = self.getPositions("full")
        try:
            int(words[0])
        except ValueError:
            self.cancelAction()

        if int(words[0]) in range(len(fullPositions)):
            self.stack.append(fullPositions[int(words[0])])
            self.currentQuery = QueryType.REMOVE_ROW_CONFIRM
            return True

        print("Nesprávne číslo!")
        return True

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
        if len(words) != 1:
            return False
        fullPositions = self.getPositions("full")
        try:
            int(words[0])
        except ValueError:
            self.cancelAction()

        if int(words[0]) in range(len(fullPositions)):
            self.stack.append(fullPositions[int(words[0])])
            self.currentQuery = QueryType.CHANGE_ROW_PRICE_NEW_PRICE
            return True

        print("Nesprávne číslo!")
        return True

    def changePrice(self, words):
        def isCorrectNumber(num):
            try:
                return float(num) > 0
            except ValueError:
                return False

        if len(words) != 1:
            return False

        if isCorrectNumber(words[0]):
            self.stack.append(float(words[0]))
            return self.finishChangingPrice()

        print("Cena tovaru musí byť kladné číslo!")
        return True

    def finishChangingPrice(self):
        price = self.stack.pop()
        row, col = self.stack.pop()
        self.automat.getRow(row, col).price = price
        return False

    def startChangingRowQuantity(self):
        self.currentQuery = QueryType.CHANGE_ROW_QUANTITY
        return True

    def selectRowToChangeQuantity(self, words):
        if len(words) != 1:
            return False
        fullPositions = self.getPositions("full")
        try:
            int(words[0])
        except ValueError:
            self.cancelAction()

        if int(words[0]) in range(len(fullPositions)):
            self.stack.append(fullPositions[int(words[0])])
            self.currentQuery = QueryType.CHANGE_ROW_QUANTITY_NEW_QUANTITY
            return True

        print("Nesprávne číslo!")
        return True

    def changeQuantity(self, words):
        def isCorrectNumber(num):
            try:
                return int(num) >= 0
            except ValueError:
                return False

        if len(words) != 1:
            return False

        if isCorrectNumber(words[0]):
            self.stack.append(int(words[0]))
            return self.finishChangingQuantity()

        print("Množstvo tovaru musí byť kladné celé číslo!")
        return True

    def finishChangingQuantity(self):
        quantity = self.stack.pop()
        row, col = self.stack.pop()
        self.automat.getRow(row, col).quantity = quantity
        return False

    def selectRowToBuy(self, words):
        if len(words) != 1:
            return False
        fullPositions = self.getPositions("full")
        try:
            int(words[0])
        except ValueError:
            self.cancelAction()

        if int(words[0]) in range(len(fullPositions)):
            self.stack.append(fullPositions[int(words[0])])
            self.currentQuery = QueryType.BUY_ROW_SELECT_PAYMENT
            return True

        print("Nesprávne číslo!")
        return True

    def selectPayment(self, words):
        if len(words) != 1:
            return False

        choice = words[0].strip()

        if choice == "0":
            return self.payWithCard()
        elif choice == "1":
            return self.payWithCash()

        print("Nesprávne číslo!")
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
        if len(words) != 1:
            return False

        try:
            int(words[0])
        except ValueError:
            self.cancelAction()

        volba = int(words[0])

        if volba not in [0,1,2,3,4,5,6,7,10,11]:
            print("Nesprávne číslo!")
            return True

        mince = {
            0: "2e",
            1: "1e",
            2: "50c",
            3: "20c",
            4: "10c",
            5: "5c",
            6: "2c",
            7: "1c"
        }

        if volba in mince:
            if not self.automat.cashRegister.insertCoin(mince[volba]):
                print("Nepodarilo sa vložiť minciu!")
                self.currentQuery = QueryType.PAY_WITH_CASH_INSERT_COINS
                return True
            return True

        if volba == 10:
            return self.finishCashPayment()

        if volba == 11:
            self.cancelAction()
            return False

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
