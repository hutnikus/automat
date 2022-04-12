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

    def testNastavTovarZaStlpec2(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.nastavRad(2, 3, "COKE", 1.5, 5), False)

    def testKatalog(self):
        automat = Automat(2, 3)
        automat.nastavRad(1, 1, "COKE", 1.5, 5)
        automat.nastavRad(0, 1, "HORALKA", 5.5, 5)
        automat.nastavRad(0, 0, "KAVENKA", 0.01, 5)
        automat.nastavRad(1, 0, "FREYER", 999.99, 5)

        katalog = automat.getKatalog()
        controlKatalog = "[0,0] - KAVENKA ($0.01)\n" \
                         "[0,1] - HORALKA ($5.50)\n" \
                         "[1,0] - FREYER ($999.99)\n" \
                         "[1,1] - COKE ($1.50)\n"

        self.assertEqual(katalog, controlKatalog)


class AutomatDataTest(unittest.TestCase):
    def testGetData(self):
        automat = Automat(1, 2)
        automat.nastavRad(0, 1, "COKE", 1.5, 5)
        automat.kasa.buffer["2e"] += 10
        automat.kasa.ucet += 10

        data = {
            'rady': [
                [None, {'pocet': 5, 'cena': '1.50', 'tovar': 'COKE'}]
            ],
            'kasa': {
                'buffer': {'2e': 10, '1e': 0, '50c': 0, '20c': 0, '10c': 0, '5c': 0, '2c': 0, '1c': 0},
                'mince': {'2e': 0, '1e': 0, '50c': 0, '20c': 0, '10c': 0, '5c': 0, '2c': 0, '1c': 0},
                'ucet': '10.00'
            }
        }

        self.assertDictEqual(data, automat.getData())

    def testLoadFromData(self):
        automat = Automat(1, 2)
        automat.nastavRad(0, 1, "COKE", 1.5, 5)
        automat.kasa.buffer["2e"] += 10
        automat.kasa.ucet += 10

        data = automat.getData()
        controlAutomat = Automat(1, 2)
        controlAutomat.loadFromData(data)

        self.assertEqual(automat, controlAutomat)

    def testSave(self):
        automat = Automat(1, 2)
        automat.nastavRad(0, 1, "COKE", 1.5, 5)
        automat.kasa.buffer["2e"] += 10
        automat.kasa.ucet += 10

        controlString = '{"rady": [[null, {"pocet": 5, "cena": "1.50", "tovar": "COKE"}]], "kasa": {"buffer": {"2e": ' \
                        '10, "1e": 0, "50c": 0, "20c": 0, "10c": 0, "5c": 0, "2c": 0, "1c": 0}, "mince": {"2e": 0, ' \
                        '"1e": 0, "50c": 0, "20c": 0, "10c": 0, "5c": 0, "2c": 0, "1c": 0}, "ucet": "10.00"}}'

        filename = "../files/data.json"
        automat.save(filename)
        with open(filename, "r") as file:
            string = file.read()

        self.assertEqual(string, controlString)

    def testLoad(self):
        automat = Automat(1, 2)
        automat.nastavRad(0, 1, "COKE", 1.5, 5)
        automat.kasa.buffer["2e"] += 10
        automat.kasa.ucet += 10

        filename = "../files/data.json"
        automat.save(filename)

        controlAutomat = Automat(1, 2)
        controlAutomat.load(filename)

        self.assertEqual(automat, controlAutomat)

    def testLoadWithDifferentSize(self):
        automat = Automat(1, 2)
        automat.nastavRad(0, 1, "COKE", 1.5, 5)
        automat.kasa.buffer["2e"] += 10
        automat.kasa.ucet += 10

        filename = "../files/data.json"
        automat.save(filename)

        controlAutomat = Automat(5, 5)
        controlAutomat.load(filename)

        self.assertEqual(automat, controlAutomat)


if __name__ == '__main__':
    unittest.main()
