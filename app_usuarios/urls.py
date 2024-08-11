from rest_framework import routers
from .api import user_viewset


router = routers.DefaultRouter()

router.register('api/users',user_viewset,'User')

urlpatterns = router.urls
