from django.urls import path, include
from rest_framework.routers import SimpleRouter
from app.views import CustomerViewset, ProductViewset, OrderViewset

router = SimpleRouter()
router.register(r'customers', CustomerViewset)
router.register(r'products', ProductViewset)
router.register(r'orders', OrderViewset)

urlpatterns = router.urls
