from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register('breeds/writable_pk', views.BreedViewSetWithWritablePK)
router.register('breeds/separate_pk', views.BreedViewSetWithSeparateIDField)
router.register(
    'breeds/nested_field', views.BreedViewSetWithWritableNestedField,
)
router.register('species', views.SpeciesViewSet)
router.register('clients', views.ClientViewSet)
router.register('animals', views.AnimalViewSet)

urlpatterns = router.urls
