from modules.console import Console
from modules.automat import Automat

automat = Automat(2, 2)
automat.cashRegister.coins = {
            "2e": 10,
            "1e": 10,
            "50c": 10,
            "20c": 10,
            "10c": 10,
            "5c": 10,
            "2c": 10,
            "1c": 10,
        }

automat.addRow(0, 0, "KEKSIK", 1.2, 3)

console = Console(automat)
