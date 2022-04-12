import unittest
from modules.automat import Automat


class AutomatTest(unittest.TestCase):
    def test_spravne2dpole(self):
        a = Automat(2, 3)
        a.rady[0][0] = 0

        test_list = [[0, None, None], [None, None, None]]

        self.assertListEqual(a.rady, test_list)

    def testNastavTovarSpravny(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.nastavRad(1, 1, "COKE", 1.5, 5), True)

    def testNastavTovarZaRiadok(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.nastavRad(2, 1, "COKE", 1.5, 5), False)

    def testNastavTovarPredRiadok(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.nastavRad(-1, 1, "COKE", 1.5, 5), False)

    def testNastavTovarPredStlpec(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.nastavRad(2, -1, "COKE", 1.5, 5), False)

    def testNastavTovarZaStlpec(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.nastavRad(2, 3, "COKE", 1.5, 5), False)

    def testNastavTovarZaStlpec(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.nastavRad(2, 3, "COKE", 1.5, 5), False)

    def testKatalog(self):
        automat = Automat(2, 3)
        automat.nastavRad(1, 1, "COKE", 1.5, 5)
        automat.nastavRad(0, 1, "HORALKA", 5.5, 5)
        automat.nastavRad(0, 0, "KAVENKA", 0.01, 5)
        automat.nastavRad(1, 0, "FREYER", 999.99, 5)

        automat.katalog()


if __name__ == '__main__':
    unittest.main()
