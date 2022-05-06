import unittest
from modules.row import Row
from decimal import Decimal


class RowTest(unittest.TestCase):
    def test_uprava_ceny(self):
        r = Row(0, Decimal(1), "keksik")

        r.setPrice(Decimal(11))

        self.assertEqual(r.price, Decimal(11))

    def test_cena_0(self):
        self.assertRaises(ValueError, Row, 0, 0, "keksik")

    def test_prazdne_meno(self):
        self.assertRaises(ValueError, Row, 0, 1, "")


class RadDataTest(unittest.TestCase):
    def testGetdata(self):
        rad = Row(1, Decimal(5.2148), "keksik")

        data = rad.getData()
        checkData = {
            "quantity": 1,
            "price": "5.21",
            "goods": "keksik"
        }

        self.assertDictEqual(data, checkData)

    def testGetdata2(self):
        rad = Row(1, Decimal(5), "keksik")

        data = rad.getData()
        checkData = {
            "quantity": 1,
            "price": "5.00",
            "goods": "keksik"
        }

        self.assertDictEqual(data, checkData)

    def testLoadFromData(self):
        rad = Row(1, Decimal(5), "keksik")
        data = {
            "quantity": 1,
            "price": "5.00",
            "goods": "keksik"
        }

        checkRad = Row(0, Decimal(0.1), "aaaaaaaa")
        checkRad.loadFromData(data)

        self.assertEqual(rad, checkRad)

    def testCreateFromData(self):
        rad = Row(1, Decimal(5), "keksik")
        data = {
            "quantity": 1,
            "price": "5.00",
            "goods": "keksik"
        }

        checkRad = Row.createFromData(data)

        self.assertEqual(rad, checkRad)


if __name__ == '__main__':
    unittest.main()
