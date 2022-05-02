import unittest

from modules.automat import Automat
from modules.console import Console, Mode, QueryType, ResetError
from modules.row import Row
from decimal import Decimal


class ConsoleTest(unittest.TestCase):
    def testStartModeSelection(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.mode = Mode.USER

        self.assertEqual(console.currentQuery, QueryType.COMMAND)
        console.executeCommand("0")
        self.assertEqual(console.currentQuery, QueryType.SET_USER_MODE)
        console.executeCommand("1")
        self.assertEqual(console.currentQuery, QueryType.COMMAND)

        self.assertEqual(console.mode, Mode.ADMIN)

    def testSetModeToAdmin(self):
        automat = Automat(2, 2)
        console = Console(automat, False)

        self.assertTrue(console.setMode(["1"]))

        self.assertEqual(console.getCurrentMode(), "admin")

    def testEmptyPositions(self):
        automat = Automat(2, 1)
        automat.addRow(1, 0, "KEKSIK", 1, 0)
        console = Console(automat, False)

        self.assertEqual(console.getPositions("empty"), [(0, 0)])

    def testGetGoods(self):
        automat = Automat(2, 1)
        console = Console(automat, False)

        self.assertEqual(console.getGoods(), "Rozmer automatu | výška: 2, šírka: 1\nPrázdny automat!")

        automat.addRow(1, 0, "KEKSIK", 1, 0)
        self.assertEqual(console.getGoods(), "Rozmer automatu | výška: 2, šírka: 1\n[1,0] - KEKSIK (1.00€) - 0ks\n")


class ConsoleAddRowTest(unittest.TestCase):

    def testAddCorrectRow(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")

        controlRow = Row(0, Decimal(1.25), "KEKSIK")

        console.executeCommand("10")
        console.executeCommand("0")
        console.executeCommand("KEKSIK")
        console.executeCommand("1.25")

        self.assertEqual(automat.getRow(0, 0), controlRow)

    def testExecuteEmptyCommand(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")

        console.executeCommand("10")
        console.executeCommand("0")

        self.assertRaises(ResetError, console.executeCommand, "")

    def testAddRowIncorrectPrice(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")

        console.executeCommand("10")
        console.executeCommand("0")
        console.executeCommand("KEKSIK")
        console.executeCommand("-1.25")
        self.assertEqual(console.currentQuery, QueryType.ADD_ROW_SET_PRICE)
        console.executeCommand("0")
        self.assertEqual(console.currentQuery, QueryType.ADD_ROW_SET_PRICE)
        console.executeCommand("fawfawf")
        self.assertEqual(console.currentQuery, QueryType.ADD_ROW_SET_PRICE)

        self.assertRaises(ResetError, console.executeCommand, "")


class ConsoleRemoveRow(unittest.TestCase):
    def testRemoveRow(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 0)

        # start renoval
        console.executeCommand("11")
        # choose row
        console.executeCommand("0")
        # confirm
        console.executeCommand("1")

        self.assertIsNone(automat.getRow(0, 0))

    def testIncorrectPosition(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 0)

        # start renoval
        console.executeCommand("11")
        # choose incorrect row
        console.executeCommand("1")

        self.assertEqual(console.currentQuery, QueryType.REMOVE_ROW_CHOOSE_ROW)
        # choose correct row
        console.executeCommand("0")
        # confirm
        console.executeCommand("1")

        self.assertIsNone(automat.getRow(0, 0))

    def testCancelChoosing(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 0)

        # start renoval
        console.executeCommand("11")
        # choose row
        console.executeCommand("0")
        # cancel
        console.executeCommand("0")

        self.assertEqual(console.currentQuery, QueryType.REMOVE_ROW_CHOOSE_ROW)
        self.assertRaises(ResetError, console.executeCommand, "")


class TestChangePrice(unittest.TestCase):
    def testChangePrice(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 0)

        # start changing price
        console.executeCommand("12")
        # choose row
        console.executeCommand("0")
        # set price
        console.executeCommand("5")

        self.assertEqual(automat.getRow(0, 0).price, 5)

    def testIncorrectPrice(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 0)

        # start changing price
        console.executeCommand("12")
        # choose incorrect row
        console.executeCommand("1")

        self.assertEqual(console.currentQuery, QueryType.CHANGE_ROW_PRICE)

        # choose correct row
        console.executeCommand("0")

        # set incorrect price
        console.executeCommand("-5")

        self.assertEqual(console.currentQuery, QueryType.CHANGE_ROW_PRICE_NEW_PRICE)

        # set correct price
        console.executeCommand("5")

        self.assertEqual(automat.getRow(0, 0).price, 5)


class TestChangeQuantity(unittest.TestCase):
    def testChangeQuantity(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 0)

        # start changing quantity
        console.executeCommand("13")
        # choose row
        console.executeCommand("0")
        # set quantity
        console.executeCommand("5")

        self.assertEqual(automat.getRow(0, 0).quantity, 5)

    def testIncorrectQuantity(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 0)

        # start changing quantity
        console.executeCommand("13")
        # choose incorrect row
        console.executeCommand("1")

        self.assertEqual(console.currentQuery, QueryType.CHANGE_ROW_QUANTITY)

        # choose correct row
        console.executeCommand("0")

        # set incorrect quantity
        console.executeCommand("-5")

        self.assertEqual(console.currentQuery, QueryType.CHANGE_ROW_QUANTITY_NEW_QUANTITY)

        # set correct quantity
        console.executeCommand("5")

        self.assertEqual(automat.getRow(0, 0).quantity, 5)


class TestCardPayment(unittest.TestCase):
    def testCardPayment(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 1)

        self.assertEqual(automat.getRow(0, 0).quantity, 1)
        self.assertEqual(automat.cashRegister.account, 0)

        # start buying
        console.executeCommand("2")
        # choose row
        console.executeCommand("0")
        # pay with card
        console.executeCommand("0")

        self.assertEqual(automat.getRow(0, 0).quantity, 0)
        self.assertEqual(automat.cashRegister.account, 1)

    def testWrongCardPayment(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1, 1)

        self.assertEqual(automat.getRow(0, 0).quantity, 1)
        self.assertEqual(automat.cashRegister.account, 0)

        # start buying
        console.executeCommand("2")
        # choose wrong row
        console.executeCommand("-1")
        # choose row
        console.executeCommand("0")
        # wrong payment type
        console.executeCommand("2")

        self.assertEqual(automat.getRow(0, 0).quantity, 1)






if __name__ == '__main__':
    unittest.main()
