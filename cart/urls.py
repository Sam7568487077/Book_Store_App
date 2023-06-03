from rest_framework.routers import DefaultRouter
from .views import ItemsCart,OrderApi,PurchaseApi

router = DefaultRouter()

# register Books view wit router
router.register('cart', ItemsCart, basename='cart')
router.register('status', OrderApi, basename='status')
router.register('purchase', PurchaseApi, basename='purchase')
urlpatterns = router.urls

