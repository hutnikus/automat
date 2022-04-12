from modules.automat import Automat
from enum import Enum


class Mode(Enum):
    USER = 0
    ADMIN = 1


class QueryType(Enum):
    COMMAND = 0
    SET_USER_MODE = 1
    CHOOSE_EMPTY_POSITION = 2


class ResetError(Exception):
    pass


class Console:
    def __init__(self, automat: Automat, looping=True):
        self.automat = automat
        self.mode = Mode.USER
        self.looping = looping
        self.currentQuery = QueryType.COMMAND
        self.startListenLoop()

    def startListenLoop(self):
        while self.looping:
            print(self.getCommandsList())
            command = input(self.getQueryText())
            try:
                self.executeCommand(command)
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
        elif self.currentQuery == QueryType.SET_USER_MODE:
            commands += "0 - mód zákazník\n"
            commands += "1 - mód admin\n"
        elif self.currentQuery == QueryType.CHOOSE_EMPTY_POSITION:
            commands += "VOĽNÉ POZÍCIE:\n"
            for i, pos in enumerate(self.getEmptyPositions()):
                commands += f"{i} - {pos}\n"
        return commands[:-1]

    def getQueryText(self):
        if self.currentQuery == QueryType.COMMAND:
            return "Zadaj príkaz: "
        if self.currentQuery == QueryType.SET_USER_MODE:
            return "Mód: "
        if self.currentQuery == QueryType.CHOOSE_EMPTY_POSITION:
            return "Pozícia: "

        return ""

    def executeCommand(self, command: str) -> bool:
        words = command.split()
        if not words or words[0] == "":
            self.cancelAction()
        if self.currentQuery == QueryType.COMMAND:
            if words[0] == "0":
                self.currentQuery = QueryType.SET_USER_MODE
                return True
            if words[0] == "1":
                print(self.getGoods())
                return True

            if self.mode == Mode.ADMIN:
                if words[0] == "10":
                    self.startAddingRows()
        if self.currentQuery == QueryType.SET_USER_MODE:
            return self.setMode(words)
        if self.currentQuery == QueryType.CHOOSE_EMPTY_POSITION:
            return self.choosePositionToAddRow(words)

        return False

    def setMode(self, words):
        if int(words[0]) in (0, 1):
            self.mode = Mode(int(words[0]))
            self.currentQuery = QueryType.COMMAND
            return True
        return False

    def getGoods(self):
        retStr = f"Rozmer automatu | vyska: {len(self.automat.items)}, sirka: {len(self.automat.items[0])}\n"
        retStr += self.automat.getCatalog()
        return retStr

    def getEmptyPositions(self) -> list:
        retList = []
        for i in range(len(self.automat.items)):
            for j in range(len(self.automat.items[0])):
                if self.automat.items[i][j] is None:
                    retList.append((i, j))
        return retList

    def startAddingRows(self):
        self.currentQuery = QueryType.CHOOSE_EMPTY_POSITION

    def choosePositionToAddRow(self, words):
        emptyPositions = self.getEmptyPositions()
        if int(words[0]) in range(len(emptyPositions)):
            if self.createAndAddRowInstance(emptyPositions[int(words[0])]):
                self.currentQuery = QueryType.COMMAND
        return False

    def cancelAction(self):
        print()
        print("Akcia prerušená!")
        self.currentQuery = QueryType.COMMAND
        raise ResetError()

    def createAndAddRowInstance(self, position): #todo refactor this
        def isCorrectNumber(num):
            try:
                return float(num) > 0
            except ValueError:
                return False

        name = input("Zadaj meno tovaru: ")
        if not name:
            self.cancelAction()

        while True:
            price = input("Zadaj cenu tovaru: ")
            if isCorrectNumber(price):
                break
            print("Cena tovaru musí byť kladné číslo!")

        price = float(price)

        return self.automat.addRow(position[0], position[1], name, price, 0)




