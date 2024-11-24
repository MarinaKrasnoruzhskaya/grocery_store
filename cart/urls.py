from django.urls import path

from cart.apps import CartConfig
from cart.views import CartAPIView, CartCleanAPIView, CartProductAPIView

app_name = CartConfig.name

urlpatterns = [
    path('', CartAPIView.as_view(), name="cart-product-list"),
    path('clean/', CartCleanAPIView.as_view(), name="cart-clean"),
    path('cart_product/', CartProductAPIView.as_view(), name="cart-product")
]
