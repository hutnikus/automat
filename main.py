from modules.console import Console
from modules.automat import Automat

automat = Automat(2, 2)

automat.addRow(0, 0, "KEKSIK", 1.2, 3)

console = Console(automat)
