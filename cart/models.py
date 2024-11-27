from django.db import models

from catalog.models import Product
from config.settings import AUTH_USER_MODEL


class Cart(models.Model):
    """ Класс для модели Корзина """

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='корзина пользователя',
        related_name='cart'
    )
    total_quantity = models.PositiveIntegerField(
        verbose_name="Количество товаров в корзине",
        default=0
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость продуктов",
        default=0.00
    )

    def __str__(self):
        return f'Корзина пользователя {self.user}'

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
        ordering = ('-id',)


class CartProduct(models.Model):
    """ Класс для модели Продукт в корзине """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='cart_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='продукт в корзине',
        related_name='cart_product'
    )
    price_cart = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость продукта',
        default=0.00)
    quantity = models.PositiveIntegerField(
        verbose_name='Количество продукта в корзине',
        default=1
    )

    def __str__(self):
        return f'{self.product.name} в корзине {self.quantity} шт.'

    class Meta:
        verbose_name = 'продукт в корзине'
        verbose_name_plural = 'продукты в корзине'
        ordering = ('-id',)
