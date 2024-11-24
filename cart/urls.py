from django.urls import path
from rest_framework.routers import SimpleRouter

from cart.apps import CartConfig
from cart.views import CartAPIView, CartCleanAPIView, CartProductViewSet

# from cart.views import CartRetrieveAPIView, CartProductCreateAPIView, CartUpdateAPIView, CartProductDestroyAPIView, \
#     CartCleanAPIView

app_name = CartConfig.name

router = SimpleRouter()
router.register(r"cart_products", CartProductViewSet, basename='cart-products')

urlpatterns = [
    path('', CartAPIView.as_view(), name="cart-product-list"),
    path('clean/', CartCleanAPIView.as_view(), name="cart-clean"),
]

urlpatterns += router.urls
