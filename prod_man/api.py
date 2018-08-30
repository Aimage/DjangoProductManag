from rest_framework import routers
from api import views as product_view

router = routers.DefaultRouter()
router.register(r'product', product_view.ProductViewset, base_name="product")
router.register(r'category', product_view.CategoryViewset,  base_name="category")
