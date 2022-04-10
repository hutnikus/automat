import unittest
from modules.rad import Rad
from decimal import Decimal


class RadTest(unittest.TestCase):
    def test_uprava_ceny(self):
        r = Rad(0, Decimal(1), "keksik")

        r.cena += 10

        self.assertEqual(r.cena, Decimal(11))

    def test_cena_0(self):
        self.assertRaises(ValueError, Rad, 0, 0, "keksik")

    def test_prazdne_meno(self):
        self.assertRaises(ValueError, Rad, 0, 1, "")

    def testGetdata(self):
        rad = Rad(1,Decimal(5.2148),"keksik")

        data = rad.getData()
        checkData = {
            "pocet": 1,
            "cena": "5.21",
            "tovar": "keksik"
        }

        self.assertDictEqual(data,checkData)

    def testGetdata2(self):
        rad = Rad(1,Decimal(5),"keksik")

        data = rad.getData()
        checkData = {
            "pocet": 1,
            "cena": "5.00",
            "tovar": "keksik"
        }

        self.assertDictEqual(data,checkData)

    def testCreateFromData(self):
        rad = Rad(1,Decimal(5),"keksik")
        data = {
            "pocet": 1,
            "cena": "5.00",
            "tovar": "keksik"
        }

        checkRad = Rad.createFromData(data)

        self.assertEqual(rad, checkRad)



if __name__ == '__main__':
    unittest.main()

