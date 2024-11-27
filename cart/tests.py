from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart, CartProduct
from catalog.models import Category, Product, ProductImage
from catalog.services import get_test_file
from users.models import User


class CartTestCase(APITestCase):

    def setUp(self):
        self.maxDiff = None
        self.user = User.objects.create(email='test@test.com', password='123456')
        self.user_2 = User.objects.create(email='test_2@test.com', password='123456')
        self.client.force_authenticate(user=self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name='Категория тест', image=get_test_file('test.webp'))
        self.subcategory = Category.objects.create(
            category=self.category,
            name='Подкатегория тест',
            image=get_test_file('test.webp')
        )
        self.subcategory_2 = Category.objects.create(
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
        self.product_2 = Product.objects.create(
            subcategory=self.subcategory,
            name='Продукт тест_2',
            price=100
        )
        self.product_images_2 = [
            ProductImage.objects.create(product=self.product_2, image=get_test_file('test.webp')),
            ProductImage.objects.create(product=self.product_2, image=get_test_file('test_2.jpeg')),
            ProductImage.objects.create(product=self.product_2, image=get_test_file('test_3.webp'))
        ]
        self.cart_product = CartProduct.objects.create(
            cart=self.cart, product_id=self.product.id, quantity=5, price_cart=self.product.price
        )
        self.quantity = 10

    def test_cart(self):
        url = reverse("cart:cart-product-list")
        response = self.client.get(url)
        data = response.json()
        images = [{'image': image.image.url} for image in self.product_images]
        result = {
            'user': {'email': self.user.email},
            'cart_products': [
                {'product': {
                    'name': self.cart_product.product.name,
                    'slug': self.cart_product.product.slug,
                    'category': self.cart_product.product.subcategory.category.name,
                    'subcategory': self.cart_product.product.subcategory.name,
                    'price': str(self.cart_product.product.price),
                    'product_images': images
                },
                    'price_cart': f"{self.cart_product.price_cart}.00",
                    'quantity': self.cart_product.quantity
                }
            ],
            'total_quantity': sum([p.quantity for p in self.cart.cart_products.all()]),
            'total_cost': float(sum([p.quantity * p.product.price for p in self.cart.cart_products.all()]))
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )

    def test_cart_another_user(self):
        self.client.force_authenticate(user=self.user_2)
        url = reverse("cart:cart-product-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_cart_clean(self):
        url = reverse("cart:cart-clean")
        response = self.client.patch(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            CartProduct.objects.filter(cart=self.user.cart).count(),
            0
        )

    def test_cart_product_add(self):
        url = reverse("cart:cart-product")
        data = {
            "product_id": self.product_2.id,
            "quantity": self.quantity
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            CartProduct.objects.filter(cart=self.user.cart).get(product_id=self.product_2.id).quantity,
            self.quantity
        )

    def test_cart_product_delete(self):
        url = reverse("cart:cart-product")
        data = {
            "product_id": self.product.id,
            "quantity": 0
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_cart_product_update(self):
        url = reverse("cart:cart-product")
        data = {
            "product_id": self.product.id,
            "quantity": self.quantity
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            CartProduct.objects.filter(cart=self.user.cart).get(product_id=self.product.id).quantity,
            self.quantity
        )
