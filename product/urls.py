from django.urls import path
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = router.urls
