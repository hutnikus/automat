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
