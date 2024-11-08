from django.db import models

from apps.core.models import ModelBase, User
from apps.products.models import Product


# Create your models here.
class Cart(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(ModelBase):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Quantity', default=1)

    class Meta:
        db_table = 'cart_item'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f'{self.product_id} - {self.quantity}'

    def get_subtotal(self):
        return self.product.price * self.quantity