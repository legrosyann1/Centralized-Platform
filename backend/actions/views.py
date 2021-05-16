from rest_framework import viewsets, generics, permissions
from actions.models import LogAction, Action
from actions.serializers import LogActionSerializer, ActionSerializer

# Create your views here.

class ActionsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated]

class LogActionsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = LogAction.objects.all()
    serializer_class = LogActionSerializer
    permission_classes = [permissions.IsAuthenticated]
