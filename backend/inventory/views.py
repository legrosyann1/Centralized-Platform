from rest_framework import viewsets, generics, permissions
from .models import Device, DevicesComment, LogicPartition
from .serializers import DeviceSerializer, CommentsSerializer, LogicPartitionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class DevicesViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get','post'])
    def logical_partitions(self, request, pk=None):
        if request.method == 'GET':
            data = LogicPartition.objects.filter(device=pk)
            serializer = LogicPartitionSerializer(data, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = LogicPartitionSerializer(data=request.data, many=True)
            if serializer.is_valid():
                partitions = serializer.save()
                device = Device.objects.get(pk=pk)
                device.logic_partition.clear()
                for partition in partitions:
                    device.logic_partition.add(partition)
            return Response(serializer.data)

class DeviceCommentsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):
    """
    API endpoint that allows devices to be viewed or edited.
    """
    queryset = DevicesComment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]