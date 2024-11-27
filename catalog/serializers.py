from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from catalog.models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для категории со списком подкатегорий"""

    subcategory = SerializerMethodField()

    class Meta:
        model = Category
        fields = ("name", "subcategory",)

    @staticmethod
    def get_subcategory(obj) -> list[str]:
        """ Возвращает список подкатегорий категории """

        return [subcategory.name for subcategory in Category.objects.filter(category=obj)]


class ProductImageSerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для изображения продукта"""

    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для продукта с подкатегорией, категорией и списком изображений"""

    subcategory = SerializerMethodField(read_only=True)
    category = SerializerMethodField()
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("name", "slug", "category", "subcategory", "price", "product_images")

    @staticmethod
    def get_category(obj) -> str:
        """ Возвращает категорию продукта """

        return obj.subcategory.category.name

    @staticmethod
    def get_subcategory(obj) -> str:
        """ Возвращает подкатегорию продукта """

        return obj.subcategory.name
