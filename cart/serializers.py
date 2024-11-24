from rest_framework import serializers

from cart.models import CartProduct, Cart
from catalog.models import Product
from catalog.serializers import ProductSerializer
from users.serializers import UserCardSerializer


class CartProductGETSerializer(serializers.ModelSerializer):
    """ Класс сериализатор для отображения продуктов корзины """

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ('product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    """ Класс-сериализатор при отображении корзины """

    user = UserCardSerializer(read_only=True)
    cart_products = CartProductGETSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField(read_only=True)
    total_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ('user', 'cart_products', 'total_quantity', 'total_cost')
        depth = 1

    @staticmethod
    def get_total_quantity(obj) -> int:
        total = 0
        cart_products = CartProduct.objects.filter(cart=obj)
        for cart_product in cart_products:
            total += cart_product.quantity
        return total

    @staticmethod
    def get_total_cost(obj) -> float:
        total = 0
        cart_products = CartProduct.objects.filter(cart=obj)
        for cart_product in cart_products:
            product = Product.objects.get(pk=cart_product.product.pk)
            total += product.price * cart_product.quantity
        return total

    def update(self, instance, validated_data):
        """ Metod """
        for product in instance.cart_products.all():
            product.delete()
        return instance


class CartProductSerializer(serializers.ModelSerializer):
    """ Класс сериализатор для отображения продуктов корзины """

    product_id = serializers.IntegerField()

    class Meta:
        model = CartProduct
        fields = ('product_id', 'quantity')

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        product_id = validated_data['product_id']
        product = Product.objects.get(pk=product_id)
        quantity = validated_data['quantity']
        product_add_cart, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        if not created:
            product_add_cart.quantity += quantity
        else:
            product_add_cart.quantity = quantity
        product_add_cart.save()
        return product_add_cart


class CartProductUpdateSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = CartProduct
        fields = ('product_id', 'quantity')

    def update(self, instance, validated_data):
        quantity = validated_data['quantity']
        instance.quantity = quantity
        instance.save()
        return instance
