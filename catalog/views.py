from rest_framework import mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from catalog.models import Category, Product
from catalog.pagination import CustomPagination
from catalog.serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(ListAPIView):
    """ Эндпоинт для просмотра всех категорий с подкатегориями с пагинацией"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """ Возвращает только категории товаров"""

        return super().get_queryset().filter(category=None)


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Класс ViewSet для модели Product """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination
    http_method_names = ['get',]
