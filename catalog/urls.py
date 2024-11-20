from django.urls import path
from rest_framework.routers import SimpleRouter

from catalog.apps import CatalogConfig
from catalog.views import CategoryListAPIView, ProductViewSet

app_name = CatalogConfig.name

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', CategoryListAPIView.as_view(), name="category-list")
]

urlpatterns += router.urls
