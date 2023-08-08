
from rest_framework import routers
from django.urls import path, re_path, include
from .api import CatalogObject, CardObject

router = routers.DefaultRouter()

router.register(r'catalog', CatalogObject, basename="catalog")
router.register(r'card', CardObject)


urlpatterns = [
    re_path(r'^rest/', include(router.urls)),
    path('rest/card/<int:pk>/', CardObject.as_view({'get': 'retrieve'}), name='card-detail')
]