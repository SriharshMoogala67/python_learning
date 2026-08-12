class Product: 
    def __init__(self, product_id, name, stock, price): 
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.price = price 


class Inventory: 
    def __init__(self): 
        self.products = {}

    def add_product(self, product): 
        self.products[product.product_id] = product


    def find_product(self, product_id):
        return self.products.get(product_id)
        product = inventory.find_product("P001")



inventory = Inventory()

laptop = Product("P001", "Laptop", 5, 70000)

inventory.add_product(laptop)

print(inventory.products["P001"].name)

product = inventory.find_product("P001")
print(product.name)