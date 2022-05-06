import os
import unittest
from modules.automat import Automat, EmptyError, getRootDirectory, NotEnoughChangeError, NotEnoughMoneyError
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
        controlCatalog = "[0,0] - KAVENKA (0.01€) - 5ks\n" \
                         "[0,1] - HORALKA (5.50€) - 5ks\n" \
                         "[1,0] - FREYER (999.99€) - 5ks\n" \
                         "[1,1] - COKE (1.50€) - 5ks\n"

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

        controlString = '{"items": [[null, {"quantity": 5, "price": "1.50", "goods": "COKE"}]], "cashRegister": {' \
                        '"buffer": {"2e": ' \
                        '10, "1e": 0, "50c": 0, "20c": 0, "10c": 0, "5c": 0, "2c": 0, "1c": 0}, "coins": {"2e": 0, ' \
                        '"1e": 0, "50c": 0, "20c": 0, "10c": 0, "5c": 0, "2c": 0, "1c": 0}, "account": "10.00"}}'

        filename = "data.json"
        automat.save(filename)

        path = os.path.join(getRootDirectory(), "files", filename)

        with open(path) as file:
            self.assertEqual(controlString, file.read())

    def testLoad(self):
        automat = Automat(1, 2)
        automat.setRow(0, 1, "COKE", 1.5, 5)
        automat.cashRegister.buffer["2e"] += 10
        automat.cashRegister.account += 10

        filename = "data.json"
        automat.save(filename)

        controlAutomat = Automat(1, 2)
        controlAutomat.load(filename)

        self.assertEqual(automat, controlAutomat)

    def testLoadWithDifferentSize(self):
        automat = Automat(1, 2)
        automat.setRow(0, 1, "COKE", 1.5, 5)
        automat.cashRegister.buffer["2e"] += 10
        automat.cashRegister.account += 10

        filename = "data.json"
        automat.save(filename)

        controlAutomat = Automat(5, 5)
        controlAutomat.load(filename)

        self.assertEqual(automat, controlAutomat)


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

    def testPayByCash(self):
        automat = Automat(1, 1)
        automat.cashRegister.coins = fullRegister.copy()
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))

        automat.cashRegister.buffer["2e"] = 1

        change = automat.buyItemWithCash(0, 0)

        self.assertEqual(change, {'50c': 1, '20c': 2, '5c': 1})

    def testPayByCashEmpty(self):
        automat = Automat(1, 1)

        self.assertRaises(EmptyError, automat.buyItemWithCash, 0, 0)

    def testPayByCashEmpty2(self):
        automat = Automat(1, 1)
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 0))

        self.assertRaises(EmptyError, automat.buyItemWithCash, 0, 0)

    def testPayByCashNotEnough(self):
        automat = Automat(1, 1)
        automat.cashRegister.coins = fullRegister.copy()
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 1.05, 5))

        self.assertRaises(NotEnoughMoneyError, automat.buyItemWithCash, 0, 0)

    def testPayByCashNotEnough2(self):
        automat = Automat(1, 1)
        automat.cashRegister.coins = fullRegister.copy()
        self.assertTrue(automat.addRow(0, 0, "KOFOLA", 5.0, 5))

        automat.cashRegister.buffer["2e"] = 1
        automat.cashRegister.buffer["1e"] = 1
        automat.cashRegister.buffer["50c"] = 1
        automat.cashRegister.buffer["20c"] = 1
        automat.cashRegister.buffer["10c"] = 1
        automat.cashRegister.buffer["5c"] = 1
        automat.cashRegister.buffer["2c"] = 1
        automat.cashRegister.buffer["1c"] = 1

        with self.assertRaises(NotEnoughMoneyError):
            automat.buyItemWithCash(0, 0)

    def testPayCashNotEnoughChage(self):
        automat = Automat(1, 1)
        automat.addRow(0, 0, "KOFOLA", 1.05, 5)
        automat.insertCoin("2e")

        self.assertRaises(NotEnoughChangeError, automat.buyItemWithCash, 0, 0)

        self.assertEqual(automat.cashRegister.returnCoins(), {"2e": 1})


if __name__ == '__main__':
    unittest.main()
