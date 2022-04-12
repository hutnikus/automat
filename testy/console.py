import unittest

from modules.automat import Automat
from modules.console import Console, Mode, QueryType


class ConsoleTest(unittest.TestCase):
    def testDefaultMode(self):
        automat = Automat(2, 2)
        console = Console(automat, False)

        self.assertEqual(console.getCurrentMode(), "zákazník")

    def testStartModeSelection(self):
        automat = Automat(2, 2)
        console = Console(automat, False)

        self.assertEqual(console.currentQuery, QueryType.COMMAND)

        console.executeCommand("0")

        self.assertEqual(console.currentQuery, QueryType.SET_USER_MODE)

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





if __name__ == '__main__':
    unittest.main()
