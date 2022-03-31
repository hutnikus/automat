import unittest
from modules.automat import Automat


class AutomatTest(unittest.TestCase):
    def test_spravne2dpole(self):
        a = Automat(2, 3)
        a.rady[0][0] = 0

        test_list = [[0, None, None], [None, None, None]]

        self.assertListEqual(a.rady, test_list)


if __name__ == '__main__':
    unittest.main()

