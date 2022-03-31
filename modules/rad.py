from dataclasses import dataclass
from decimal import Decimal
from tovar import *


@dataclass()
class Rad:
    pocet: int
    cena: Decimal
    tovar: Tovar
