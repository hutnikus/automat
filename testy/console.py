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

        self.assertEqual(console.getEmptyPositions(), [(0, 0)])

    def testGetGoods(self):
        automat = Automat(2, 1)
        console = Console(automat, False)

        self.assertEqual(console.getGoods(), "Rozmer automatu | vyska: 2, sirka: 1\n")

        automat.addRow(1, 0, "KEKSIK", 1, 0)
        self.assertEqual(console.getGoods(), "Rozmer automatu | vyska: 2, sirka: 1\n[1,0] - KEKSIK (1.00€)\n")

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


if __name__ == '__main__':
    unittest.main()
