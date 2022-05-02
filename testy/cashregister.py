import unittest
from modules.cashregister import CashRegister, NotEnoughCoinsInRegisterException
from decimal import Decimal


class CashRegisterTest(unittest.TestCase):
    def test_spravny_dict(self):
        k = CashRegister()
        test_dict_changed = {
            "2e": 1,
            "1e": 0,
            "50c": 0,
            "20c": 0,
            "10c": 0,
            "5c": 0,
            "2c": 0,
            "1c": 0
        }
        test_dict_original = {
            "2e": 0,
            "1e": 0,
            "50c": 0,
            "20c": 0,
            "10c": 0,
            "5c": 0,
            "2c": 0,
            "1c": 0
        }

        k.buffer["2e"] += 1

        self.assertDictEqual(k.buffer, test_dict_changed)
        self.assertDictEqual(k.coins, test_dict_original)


class CashRegisterDataTest(unittest.TestCase):
    def testGetdata(self):
        kasa = CashRegister()
        kasa.buffer["2e"] += 1
        kasa.account = 11
        kasa.coins["2e"] += 1
        data = kasa.getData()
        checkData = {
            "buffer": {'10c': 0,
                       '1c': 0,
                       '1e': 0,
                       '20c': 0,
                       '2c': 0,
                       '2e': 1,
                       '50c': 0,
                       '5c': 0},
            "coins": {'10c': 0,
                      '1c': 0,
                      '1e': 0,
                      '20c': 0,
                      '2c': 0,
                      '2e': 1,
                      '50c': 0,
                      '5c': 0},
            "account": "11"
        }

        self.assertDictEqual(data, checkData)

    def testLoadFromData(self):
        originalKasa = CashRegister()
        originalKasa.account += 10
        originalKasa.coins["1e"] += 5
        originalKasa.coins["50c"] += 7
        originalKasa.coins["5c"] += 10

        data = originalKasa.getData()
        newKasa = CashRegister()
        newKasa.loadFromData(data)

        self.assertEqual(originalKasa, newKasa)

class TestCash(unittest.TestCase):
    def testGetChange(self):
        kasa = CashRegister()
        kasa.coins = {
            "2e": 10,
            "1e": 10,
            "50c": 10,
            "20c": 10,
            "10c": 10,
            "5c": 10,
            "2c": 10,
            "1c": 10,
        }

        change = kasa.getChange(Decimal("1.25"))

        self.assertEqual(kasa.getDictSum(change), Decimal("1.25"))
        self.assertDictEqual(change, {
            "1e": 1,
            "20c": 1,
            "5c": 1,
        })

    def testPayCash(self):
        kasa = CashRegister()
        kasa.coins = {
            "2e": 10,
            "1e": 10,
            "50c": 10,
            "20c": 10,
            "10c": 10,
            "5c": 10,
            "2c": 10,
            "1c": 10,
        }
        kasa.buffer["2e"] += 1

        changeValue = kasa.payCashGetChange(Decimal("1.25"))

        self.assertTrue(changeValue[1])

        change = changeValue[0]

        self.assertEqual(kasa.getDictSum(change), Decimal("0.75"))

    def testPayCashEmptyBuffer(self):
        kasa = CashRegister()
        kasa.coins = {
            "2e": 10,
            "1e": 10,
            "50c": 10,
            "20c": 10,
            "10c": 10,
            "5c": 10,
            "2c": 10,
            "1c": 10,
        }

        with self.assertRaises(ValueError):
            kasa.payCashGetChange(Decimal("1.25"))

    def testGetChangeNotEnoughMoney(self):
        kasa = CashRegister()
        kasa.buffer["2e"] += 1

        testDict = kasa.buffer.copy()

        self.assertEqual(kasa.payCashGetChange(Decimal("1.25")), (testDict, False) )

        self.assertEqual(kasa.buffer["2e"], 1)
        self.assertEqual(kasa.coins["2e"], 0)



if __name__ == '__main__':
    unittest.main()
