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
        cart = Cart.objects.get(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

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
    http_method_names = ['patch', 'delete']

    def patch(self, request):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class CartProductViewSet(ModelViewSet):
    """ Класс для работы с продуктами в корзине """

    queryset = CartProduct.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ['post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == "partial_update":
            return CartProductUpdateSerializer
        return CartProductSerializer
