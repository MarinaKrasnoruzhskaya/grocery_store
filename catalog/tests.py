from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from catalog.models import Category, Subcategory, Product, ProductImage
from catalog.services import get_test_file
from users.models import User


class CatalogTestCase(APITestCase):

    def setUp(self):
        self.maxDiff = None

        self.category = Category.objects.create(name='Категория тест', image=get_test_file('test.webp'))
        self.subcategory = Subcategory.objects.create(
            category=self.category,
            name='Подкатегория тест',
            image=get_test_file('test.webp')
        )
        self.subcategory_2 = Subcategory.objects.create(
            category=self.category,
            name='Подкатегория тест 2',
            image=get_test_file('test.webp')
        )
        self.product = Product.objects.create(
            subcategory=self.subcategory,
            name='Продукт тест',
            price=100
        )
        self.product_images = [
            ProductImage.objects.create(product=self.product, image=get_test_file('test.webp')),
            ProductImage.objects.create(product=self.product, image=get_test_file('test_2.jpeg')),
            ProductImage.objects.create(product=self.product, image=get_test_file('test_3.webp'))
        ]

    def test_category_list(self):
        url = reverse('catalog:category-list')
        response = self.client.get(url)
        data = response.json()
        subcategories = [subcategory.name for subcategory in Subcategory.objects.filter(category=self.category)]
        result = {'count': 1, 'next': None, 'previous': None,
                  'results': [{'name': self.category.name, 'subcategory': subcategories}]}

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )

    def test_products(self):
        url = reverse('catalog:products-list')
        response = self.client.get(url)
        images = [{'image': f"http://testserver{image.image.url}"} for image in self.product_images]
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'name': self.product.name,
                    'slug': self.product.slug,
                    'category': self.product.subcategory.category.name,
                    'subcategory': self.product.subcategory.name,
                    'price': f"{self.product.price}.00",
                    'product_images': images
                }
            ]
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )
