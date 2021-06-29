from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CountryViewSet, BrendViewSet, AutoViewSet


router = routers.DefaultRouter()
router.register('country_list', CountryViewSet)
router.register('brend_list', BrendViewSet)
router.register('model_auto', AutoViewSet)

urlpatterns = router.urls

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])