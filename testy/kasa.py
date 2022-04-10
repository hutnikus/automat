import unittest
from modules.kasa import Kasa


class KasaTest(unittest.TestCase):
    def test_spravny_dict(self):
        k = Kasa()
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

        self.assertDictEqual(k.buffer,test_dict_changed)
        self.assertDictEqual(k.mince,test_dict_original)


    def testGetdata(self):
        kasa = Kasa()
        kasa.buffer["2e"] += 1
        kasa.ucet = 11
        kasa.mince["2e"] += 1
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
            "mince": {'10c': 0,
            '1c': 0,
           '1e': 0,
            '20c': 0,
            '2c': 0,
            '2e': 1,
           '50c': 0,
           '5c': 0},
            "ucet": "11"
        }

        self.assertDictEqual(data, checkData)

if __name__ == '__main__':
    unittest.main()

