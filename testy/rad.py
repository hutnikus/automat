import unittest
from modules.rad import Rad
from modules.tovar import Tovar
from decimal import Decimal


class RadTest(unittest.TestCase):
    def test_uprava_ceny(self):
        r = Rad(0, Decimal(0), Tovar("keksik", "snack"))

        r.cena += 10

        self.assertEqual(r.cena, Decimal(10))


if __name__ == '__main__':
    unittest.main()

