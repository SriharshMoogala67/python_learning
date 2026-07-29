class Product:
    total_items_sold = 0
    total_sales_revenue = 0.0

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
    ):
        if not product_id.strip():
            raise ValueError("Product ID cannot be empty.")

        if not name.strip():
            raise ValueError("Product name cannot be empty.")

        if price < 0:
            raise ValueError("Price cannot be negative.")

        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        self.product_id = product_id.strip().upper()
        self.name = name.strip()
        self.price = price
        self.stock = stock

    def add_stock(self, quantity: int) -> bool:
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return False

        self.stock += quantity

        print(
            f"Added {quantity} units of {self.name}. "
            f"Current stock: {self.stock}"
        )

        return True

    def sell(self, quantity: int) -> bool:
        if quantity <= 0:
            print("Sale quantity must be greater than zero.")
            return False

        if quantity > self.stock:
            print(
                f"Insufficient stock for {self.name}. "
                f"Available stock: {self.stock}"
            )
            return False

        self.stock -= quantity
        sale_value = self.price * quantity

        Product.total_items_sold += quantity
        Product.total_sales_revenue += sale_value

        print(
            f"Sold {quantity} units of {self.name} "
            f"for £{sale_value:.2f}."
        )

        return True

    def get_inventory_value(self) -> float:
        return self.price * self.stock

    def display(self) -> None:
        print(
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: £{self.price:.2f} | "
            f"Stock: {self.stock} | "
            f"Value: £{self.get_inventory_value():.2f}"
        )


class Inventory:
    def __init__(self):
        self.products: dict[str, Product] = {}

    def add_product(self, product: Product) -> bool:
        if product.product_id in self.products:
            print("A product with this ID already exists.")
            return False

        self.products[product.product_id] = product

        print(f"{product.name} added to inventory.")
        return True

    def find_product(self, product_id: str) -> Product | None:
        return self.products.get(product_id.strip().upper())

    def sell_product(
        self,
        product_id: str,
        quantity: int,
    ) -> bool:
        product = self.find_product(product_id)

        if product is None:
            print("Product not found.")
            return False

        return product.sell(quantity)

    def restock_product(
        self,
        product_id: str,
        quantity: int,
    ) -> bool:
        product = self.find_product(product_id)

        if product is None:
            print("Product not found.")
            return False

        return product.add_stock(quantity)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)

        if product is None:
            print("Product not found.")
            return False

        del self.products[product.product_id]

        print(f"{product.name} removed from inventory.")
        return True

    def show_inventory(self) -> None:
        if not self.products:
            print("Inventory is empty.")
            return

        print("\n--- Current Inventory ---")

        for product in self.products.values():
            product.display()

    def calculate_total_inventory_value(self) -> float:
        total = 0.0

        for product in self.products.values():
            total += product.get_inventory_value()

        return total

    def show_metrics(self) -> None:
        inventory_value = self.calculate_total_inventory_value()

        print("\n--- Inventory Metrics ---")
        print(f"Total inventory value: £{inventory_value:.2f}")
        print(f"Total items sold: {Product.total_items_sold}")
        print(
            "Total sales revenue: "
            f"£{Product.total_sales_revenue:.2f}"
        )


if __name__ == "__main__":
    inventory = Inventory()

    laptop = Product("P001", "Laptop", 750.00, 10)
    mouse = Product("P002", "Wireless Mouse", 25.00, 30)
    keyboard = Product("P003", "Keyboard", 45.00, 20)

    inventory.add_product(laptop)
    inventory.add_product(mouse)
    inventory.add_product(keyboard)

    inventory.show_inventory()

    inventory.sell_product("P001", 2)
    inventory.sell_product("P002", 5)
    inventory.restock_product("P003", 10)

    inventory.show_inventory()
    inventory.show_metrics()