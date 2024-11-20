from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from catalog.models import Subcategory, Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для категории со списком подкатегорий"""

    subcategory = SerializerMethodField()

    @extend_schema_field({"type": "array", "items": Subcategory})
    def get_subcategory(self, category):
        return [subcategory.name for subcategory in Subcategory.objects.filter(category=category)]

    class Meta:
        model = Category
        fields = ("name", "subcategory",)


class SubcategorySerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для подкатегории"""

    class Meta:
        model = Subcategory
        fields = ("name",)


class ProductImageSerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для изображения продукта"""

    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductCreateSerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для создания продукта с загрузкой изображений """

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        min_length=3,
        max_length=3,
        allow_empty=False
    )

    class Meta:
        model = Product
        fields = ("subcategory", "name", "price", "uploaded_images")

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product


class ProductSerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для продукта с подкатегорией, категорией и списком изображений"""

    subcategory = SerializerMethodField(read_only=True)
    category = SerializerMethodField()
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("name", "slug", "category", "subcategory", "price", "product_images")

    def get_category(self, obj):
        return obj.subcategory.category.name

    def get_subcategory(self, obj):
        return obj.subcategory.name
