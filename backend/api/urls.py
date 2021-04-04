from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from .views import UserViewSet, GroupViewSet
from inventory.views import DevicesViewSet, DeviceCommentsViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'devices', DevicesViewSet)
router.register(r'devicesComments', DeviceCommentsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('obtain_token', obtain_jwt_token, name="api_token_auth"),
    path('refresh_token', refresh_jwt_token, name="api_token_refresh"),
]