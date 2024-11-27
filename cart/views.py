from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart, CartProduct
from cart.serializers import CartProductSerializer, CartSerializer, CartProductUpdateSerializer
from users.permissions import IsOwner


class CartAPIView(APIView):
    """ Класс для отображения содержимого корзины авторизованного пользователя """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):

        user = self.request.user
        if Cart.objects.filter(user=user).exists():
            cart = Cart.objects.get(user=user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "Нельзя просматривать чужую корзину"})

    def get_queryset(self):
        """ Получаем корзину текущего пользователя """
        user = self.request.user
        cart = Cart.objects.get(user=user)
        return cart.cart_products.all()


class CartCleanAPIView(APIView):
    """ Класс для полной очистки корзины авторизованного пользователя"""

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ['patch', 'delete', 'get']

    def patch(self, request):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=204)
        else:
            return Response(serializer.errors, status=400)


class CartProductAPIView(APIView):
    """ Класс для добавления продукта в корзину авторизованного пользователя, изменения количества или удаления """

    queryset = CartProduct.objects.all()
    serializer_class = CartProductUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ['post', 'patch', 'delete']

    def post(self, request):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        serializer = CartProductUpdateSerializer(data=request.data)

        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            product_cart, created = CartProduct.objects.get_or_create(cart=cart, product_id=product_id)
            if created and quantity:
                product_cart.quantity = quantity
                product_cart.price_cart = product_cart.product.price
                product_cart.save()
                return Response(serializer.data, status=201)
            if quantity:
                product_cart.quantity = quantity
                product_cart.price_cart = product_cart.product.price
                product_cart.save()
                data = {"product_id": product_id, "quantity": product_cart.quantity}
                return Response(data=data)
            if not quantity:
                product_cart.delete()
                return Response(status=204)
        else:
            return Response(serializer.errors, status=400)
