from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from actions.views import ScheduledTaskViewSet, ActionsViewSet, LogActionsViewSet
from .views import UserViewSet, GroupViewSet, EmailViewSet, MetricsViewSet
from inventory.views import DevicesViewSet, DeviceCommentsViewSet, DeviceChangesViewSet, FutureChangesViewSet, NetworksViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'devices', DevicesViewSet)
router.register(r'devicesComments', DeviceCommentsViewSet)
router.register(r'devicesChanges', DeviceChangesViewSet)
router.register(r'changes', FutureChangesViewSet)
router.register(r'networks', NetworksViewSet)
router.register(r'tasks', ScheduledTaskViewSet)
router.register(r'actions', ActionsViewSet)
router.register(r'logActions', LogActionsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('email',EmailViewSet.as_view(),name='email'),
    path(r'metrics/', MetricsViewSet.as_view(), name='metrics'), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('obtain_token', obtain_jwt_token, name="api_token_auth"),
    path('refresh_token', refresh_jwt_token, name="api_token_refresh"),
] 

urlpatterns += router.urls
 