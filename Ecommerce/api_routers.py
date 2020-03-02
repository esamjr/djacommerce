from rest_framework import routers
from backend.api.viewsets import item_viewset
from backend.api.viewsets import user_viewset

router = routers.DefaultRouter()
router.register(r'items', item_viewset.ItemView)
router.register(r'user', user_viewset.userviewsets)