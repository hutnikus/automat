from dataclasses import dataclass


@dataclass(frozen=True)
class Tovar:
    meno: str
    typ: str
