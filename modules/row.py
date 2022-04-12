from decimal import Decimal


class Row:
    def __init__(self, quantity: int, price: Decimal, goods: str):
        self.quantity = quantity
        if price <= 0:
            raise ValueError("Cena musí byť vyššia ako 0!")
        self.price = round(price, 2)
        if goods == '' or goods is None:
            raise ValueError("Tovar musí mať platné goodsName!")
        self.goods = goods

    def setGoods(self, newName: str) -> bool:
        if not (newName and isinstance(newName, str)):
            return False
        self.goods = newName
        return True

    def setNumber(self, newNumber: int) -> bool:
        if not (newNumber and isinstance(newNumber, bool)):
            return False
        self.quantity = newNumber
        return True

    def setPrice(self, newPrice: Decimal) -> bool:
        if not (newPrice and isinstance(newPrice, Decimal)):
            return False
        if newPrice <= 0:
            return False
        self.price = round(newPrice, 2)

    def adjustQuantity(self, amount: int) -> bool:
        if not (amount and isinstance(amount, int)):
            return False
        self.quantity += amount
        if self.quantity < 0:
            self.quantity -= amount
            return False
        return True

    def __str__(self):
        return f"{self.goods}: {self.quantity}x {self.price}"

    def __eq__(self, other):
        return (
                self.quantity == other.quantity and
                self.price == other.price and
                self.goods == other.goods
        )

    def getData(self):
        return {
            "quantity": self.quantity,
            "price": str(self.price),
            "goods": self.goods
        }

    def loadFromData(self, data):
        self.quantity = data["quantity"]
        self.price = Decimal(data["price"])
        self.goods = data["goods"]

    @staticmethod
    def createFromData(data):
        if data is None:
            return None
        return Row(
            data["quantity"],
            Decimal(data["price"]),
            data["goods"]
        )


if __name__ == '__main__':
    rad = Row(1, Decimal(5.459), "keksik")
    print(rad)
    print(round(Decimal(5.65416), 3).__repr__())
