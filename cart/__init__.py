import json

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Parse JSON contents instead of using eval()
    items = [json.loads(cart_detail['contents']) for cart_detail in cart_details]
    
    # Flatten the list of items
    product_ids = [item for sublist in items for item in sublist]

    # Fetch all products in one DB call instead of looping
    products_list = products.get_products_bulk(product_ids)  # Assuming a bulk-fetch function exists

    return products_list

    


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)


