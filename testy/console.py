import unittest
from modules.automat import Automat
from modules.console import Console, Mode, QueryType, ResetError
from modules.row import Row
from decimal import Decimal

fullRegister = {
    "2e": 10,
    "1e": 10,
    "50c": 10,
    "20c": 10,
    "10c": 10,
    "5c": 10,
    "2c": 10,
    "1c": 10,
}


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


class TestCashPayment(unittest.TestCase):
    def testCashPayment(self):
        automat = Automat(2, 2)
        automat.cashRegister.coins = fullRegister.copy()
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1.25, 1)

        startSum = automat.cashRegister.getCoinsSum()

        # start buying
        console.executeCommand("2")
        # choose row
        console.executeCommand("0")
        # pay with cash
        console.executeCommand("1")
        # insert 2e
        console.executeCommand("0")

        self.assertEqual(automat.cashRegister.getBufferSum(), Decimal(2.00))

        # finish paying
        console.executeCommand("10")

        self.assertEqual(startSum + Decimal(1.25), automat.cashRegister.getCoinsSum())

    def testCashPaymentNotEnoughCashBack(self):
        automat = Automat(2, 2)
        automat.cashRegister.coins["50c"] += 1
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1.25, 1)

        startSum = automat.cashRegister.getCoinsSum()

        # start buying
        console.executeCommand("2")
        # choose row
        console.executeCommand("0")
        # pay with cash
        console.executeCommand("1")
        # insert 2e
        console.executeCommand("0")

        self.assertEqual(automat.cashRegister.getBufferSum(), Decimal(2.00))

        # finish paying
        with self.assertRaises(ResetError):
            console.executeCommand("10")

        # no money was taken
        self.assertEqual(startSum, automat.cashRegister.getCoinsSum())

        # console back to default
        self.assertEqual(console.currentQuery.value, 0)

    def testCashPaymentNotEnoughInserted(self):
        automat = Automat(2, 2)
        automat.cashRegister.coins = fullRegister.copy()
        console = Console(automat, False)
        console.setMode("1")
        automat.addRow(0, 0, "KEKSIK", 1.25, 1)

        startSum = automat.cashRegister.getCoinsSum()

        # start buying
        console.executeCommand("2")
        # choose row
        console.executeCommand("0")
        # pay with cash
        console.executeCommand("1")
        # insert 1e
        console.executeCommand("1")

        self.assertEqual(automat.cashRegister.getBufferSum(), Decimal(1.00))

        # finish paying
        console.executeCommand("10")

        # no money was taken
        self.assertEqual(startSum, automat.cashRegister.getCoinsSum())
        # buffer still intact
        self.assertEqual(automat.cashRegister.getBufferSum(), Decimal(1.00))

        # cancel payment
        with self.assertRaises(ResetError):
            console.executeCommand("")

        # buffer empty
        self.assertEqual(automat.cashRegister.getBufferSum(), Decimal(0.00))
        # still, no money was taken
        self.assertEqual(startSum, automat.cashRegister.getCoinsSum())


class TestChangeRegister(unittest.TestCase):
    def testChangeRegister(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")

        # start changing register
        console.executeCommand("14")

        self.assertEqual(automat.cashRegister.coins["2e"], 0)

        # select 2e
        console.executeCommand("0")

        # check selected query
        self.assertEqual(console.currentQuery.value, 15)

        # change amount to 10
        console.executeCommand("10")

        self.assertEqual(automat.cashRegister.coins["2e"], 10)

        self.assertEqual(console.currentQuery.value, 14)

    def testWrongInput(self):
        automat = Automat(2, 2)
        console = Console(automat, False)
        console.setMode("1")

        # start changing register
        console.executeCommand("14")
        self.assertEqual(automat.cashRegister.coins["2e"], 0)
        # select 2e
        console.executeCommand("0")

        # change amount to -5
        console.executeCommand("-5")

        # see if register unchanged
        self.assertEqual(automat.cashRegister.coins["2e"], 0)
        self.assertEqual(console.currentQuery.value, 15)

        console.executeCommand("1.5")

        # see if register unchanged
        self.assertEqual(automat.cashRegister.coins["2e"], 0)
        self.assertEqual(console.currentQuery.value, 15)


if __name__ == '__main__':
    unittest.main()
