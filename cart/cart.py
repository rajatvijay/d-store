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
