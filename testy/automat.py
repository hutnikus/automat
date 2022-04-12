import unittest
from modules.automat import Automat


class AutomatTest(unittest.TestCase):
    def test_spravne2dpole(self):
        a = Automat(2, 3)
        a.items[0][0] = 0

        test_list = [[0, None, None], [None, None, None]]

        self.assertListEqual(a.items, test_list)

    def testSetCorrectGoods(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.setRow(1, 1, "COKE", 1.5, 5), True)

    def testSetCorrectGoodsOutOfBoundsMore1(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.setRow(2, 1, "COKE", 1.5, 5), False)

    def testSetCorrectGoodsOutOfBoundsLess1(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.setRow(-1, 1, "COKE", 1.5, 5), False)

    def testSetCorrectGoodsOutOfBoundsMore2(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.setRow(2, -1, "COKE", 1.5, 5), False)

    def testSetCorrectGoodsOutOfBoundsLess2(self):
        automat = Automat(2, 3)

        self.assertEqual(automat.setRow(2, 3, "COKE", 1.5, 5), False)

    def testCatalog(self):
        automat = Automat(2, 3)
        automat.setRow(1, 1, "COKE", 1.5, 5)
        automat.setRow(0, 1, "HORALKA", 5.5, 5)
        automat.setRow(0, 0, "KAVENKA", 0.01, 5)
        automat.setRow(1, 0, "FREYER", 999.99, 5)

        catalog = automat.getCatalog()
        controlCatalog = "[0,0] - KAVENKA ($0.01)\n" \
                         "[0,1] - HORALKA ($5.50)\n" \
                         "[1,0] - FREYER ($999.99)\n" \
                         "[1,1] - COKE ($1.50)\n"

        self.assertEqual(catalog, controlCatalog)


class AutomatDataTest(unittest.TestCase):
    def testGetData(self):
        automat = Automat(1, 2)
        automat.setRow(0, 1, "COKE", 1.5, 5)
        automat.cashRegister.buffer["2e"] += 10
        automat.cashRegister.account += 10

        data = {
            'items': [
                [None, {'quantity': 5, 'price': '1.50', 'goods': 'COKE'}]
            ],
            'cashRegister': {
                'buffer': {'2e': 10, '1e': 0, '50c': 0, '20c': 0, '10c': 0, '5c': 0, '2c': 0, '1c': 0},
                'coins': {'2e': 0, '1e': 0, '50c': 0, '20c': 0, '10c': 0, '5c': 0, '2c': 0, '1c': 0},
                'account': '10.00'
            }
        }

        self.assertDictEqual(data, automat.getData())

    def testLoadFromData(self):
        automat = Automat(1, 2)
        automat.setRow(0, 1, "COKE", 1.5, 5)
        automat.cashRegister.buffer["2e"] += 10
        automat.cashRegister.account += 10

        data = automat.getData()
        controlAutomat = Automat(1, 2)
        controlAutomat.loadFromData(data)

        self.assertEqual(automat, controlAutomat)

    def testSave(self):
        automat = Automat(1, 2)
        automat.setRow(0, 1, "COKE", 1.5, 5)
        automat.cashRegister.buffer["2e"] += 10
        automat.cashRegister.account += 10

        controlString = '{"items": [[null, {"quantity": 5, "price": "1.50", "goods": "COKE"}]], "cashRegister": {"buffer": {"2e": ' \
                        '10, "1e": 0, "50c": 0, "20c": 0, "10c": 0, "5c": 0, "2c": 0, "1c": 0}, "coins": {"2e": 0, ' \
                        '"1e": 0, "50c": 0, "20c": 0, "10c": 0, "5c": 0, "2c": 0, "1c": 0}, "account": "10.00"}}'

        filename = "../files/data.json"
        automat.save(filename)
        with open(filename, "r") as file:
            string = file.read()

        self.assertEqual(string, controlString)

    def testLoad(self):
        automat = Automat(1, 2)
        automat.setRow(0, 1, "COKE", 1.5, 5)
        automat.cashRegister.buffer["2e"] += 10
        automat.cashRegister.account += 10

        filename = "../files/data.json"
        automat.save(filename)

        controlAutomat = Automat(1, 2)
        controlAutomat.load(filename)

        self.assertEqual(automat, controlAutomat)

    def testLoadWithDifferentSize(self):
        automat = Automat(1, 2)
        automat.setRow(0, 1, "COKE", 1.5, 5)
        automat.cashRegister.buffer["2e"] += 10
        automat.cashRegister.account += 10

        filename = "../files/data.json"
        automat.save(filename)

        controlAutomat = Automat(5, 5)
        controlAutomat.load(filename)

        self.assertEqual(automat, controlAutomat)


if __name__ == '__main__':
    unittest.main()
