from django.conf import settings
from decimal import Decimal
from shop.models import Product

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session.get[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add product ti the cart or update its quantity
        :param product: the instance of the Product model
        :param quantity:
        :param update_quantity:
        :return:
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id][quantity] = quantity
        else:
            self.cart[product_id][quantity] += quantity

        self.save()

    def save(self):
        """
        Save the cart
        :return:
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the product ids in the  self.cart and fetch the product from the db
        :return:
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count the total no of products in the cart
        :return:
        """

        return sum([item['quantity'] for item in self.cart.values()])

    def get_total_price(self):
        """
        Get the total price of the cart
        :return:
        """
        return sum([Decimal(item['quantity']) * item['price'] for item in self.cart.values()])

    def clear(self):
        """
        Clear the cart's session
        :return:
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True