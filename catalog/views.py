from rest_framework import request, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from catalog.models import Category, Product
from catalog.pagination import CustomPagination
from catalog.serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer


class CategoryListAPIView(ListAPIView):
    """ Эндпоинт для просмотра всех категорий с подкатегориями с пагинацией"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class ProductViewSet(ModelViewSet):
    """ """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return ProductSerializer

