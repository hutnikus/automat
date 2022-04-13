import unittest
from modules.automat import Automat, EmptyError
from modules.row import Row
from decimal import Decimal


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
        controlCatalog = "[0,0] - KAVENKA (0.01€)\n" \
                         "[0,1] - HORALKA (5.50€)\n" \
                         "[1,0] - FREYER (999.99€)\n" \
                         "[1,1] - COKE (1.50€)\n"

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


    # todo chyba pri otvarani suboru


class TestGoodsManagement(unittest.TestCase):
    def testRowInsert(self):
        automat = Automat(1, 1)
        testRad = Row(5, Decimal(1.05), "KOFOLA")

        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))

        self.assertEqual(testRad, automat.getRow(0, 0))

    def testRowInsertWrongParam(self):
        automat = Automat(1, 1)

        self.assertFalse(automat.addRow(1, 0, "KOFOLA", 1.05, 5))

        self.assertEqual(None, automat.getRow(0, 0))

    def testRowInsertUsedSpace(self):
        automat = Automat(1, 1)
        testRad = Row(5, Decimal(1.05), "KOFOLA")

        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))
        self.assertFalse(automat.addRow(0, 0, "FREYER", 1.05, 5))

        self.assertEqual(testRad, automat.getRow(0, 0))

    def testRowRemove(self):
        automat = Automat(1, 1)
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))
        self.assertTrue(automat.removeRow(0, 0))
        self.assertEqual(None, automat.getRow(0, 0))

    def testRowRemoveUnused(self):
        automat = Automat(1, 1)
        self.assertFalse(automat.removeRow(0, 0))

    def testRowRemoveWrongParam(self):
        automat = Automat(1, 1)
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))
        self.assertFalse(automat.removeRow(1, 0))

    def testGetRowUsed(self):
        automat = Automat(1, 1)
        testRad = Row(5, Decimal(1.05), "KOFOLA")
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))
        self.assertEqual(automat.getRow(0, 0), testRad)

    def testGetRowUnused(self):
        automat = Automat(1, 1)
        self.assertEqual(automat.getRow(0, 0), None)

    def testGetRowOutOfBounds(self):
        automat = Automat(1, 1)
        self.assertRaises(IndexError, automat.getRow, 1, 1)


class TestPayment(unittest.TestCase):
    def testPayByCardCorrect(self):
        automat = Automat(1, 1)
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))

        self.assertTrue(automat.buyItemWithCard(0, 0))

        self.assertEqual(automat.cashRegister.account, round(Decimal(1.05), 2))
        self.assertEqual(automat.getRow(0, 0).quantity, 4)

    def testPayByCardEmpty(self):
        automat = Automat(1, 1)

        self.assertRaises(EmptyError, automat.buyItemWithCard, 0, 0)

    def testPayByCardEmpty2(self):
        automat = Automat(1, 1)
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 0))

        self.assertRaises(EmptyError, automat.buyItemWithCard, 0, 0)


if __name__ == '__main__':
    unittest.main()
