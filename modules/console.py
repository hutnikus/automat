from modules.automat import Automat
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

    def getCommandsList(self):
        commands = "#" * 20 + "\n"
        commands += f"--mód {self.getCurrentMode()}--\n"
        if self.currentQuery == QueryType.COMMAND:
            commands += "0 - nastav mód\n"
            commands += "1 - zobraz stav tovarov\n"

            if self.mode == Mode.ADMIN:
                commands += "10 - pridaj rad\n"
                commands += "11 - odstráň rad\n"
        elif self.currentQuery == QueryType.SET_USER_MODE:
            commands += "0 - mód zákazník\n"
            commands += "1 - mód admin\n"
        elif self.currentQuery == QueryType.ADD_ROW_CHOOSE_EMPTY:
            commands += "VOĽNÉ POZÍCIE:\n"
            for i, pos in enumerate(self.getPositions("empty")):
                commands += f"{i} - {pos}\n"
        elif self.currentQuery == QueryType.REMOVE_ROW_CHOOSE_ROW:
            for i, pos in enumerate(self.getGoods()[:-1].split("\n")):
                if i == 0:
                    commands += f"{pos}\n"
                    continue
                commands += f"{i-1} - {pos}\n"
        elif self.currentQuery == QueryType.REMOVE_ROW_CONFIRM:
            commands += "0 - Nie\n"
            commands += "1 - Áno, odstrániť rad.\n"
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

        return False

    def handleTypeCommand(self, words):
        if words[0] == "0":
            self.currentQuery = QueryType.SET_USER_MODE
            return True
        if words[0] == "1":
            print(self.getGoods())
            return True

        if self.mode == Mode.ADMIN:
            if words[0] == "10":
                return self.startAddingRows()
            if words[0] == "11":
                return self.startRemovingRows()

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

    def cancelAction(self):
        print()
        print("Akcia prerušená!")
        self.currentQuery = QueryType.COMMAND
        self.stack = []
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



