from rest_framework import routers 
from .api import ReporteViewSet
from .views import ReporteViewSet



router = routers.DefaultRouter()

router.register('api/reportes', ReporteViewSet,'reportes')

urlpatterns = router.urls

