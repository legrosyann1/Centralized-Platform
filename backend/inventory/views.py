from rest_framework import viewsets, generics, permissions
from .models import Device, DeviceComment, LogicPartition, Change, FutureChange, Interface, Network
from .serializers import DeviceSerializer, CommentsSerializer, InterfaceSerializer, LogicPartitionSerializer, ChangeSerializer, FutureChangeSerializer, NetworkSerializer; InterfaceSerializer, NetworkSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import os
from django.http import  HttpResponse
from wsgiref.util import FileWrapper


class DevicesViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        if type(request.data) is dict:
            serializer = DeviceSerializer(data=request.data)
        elif type(request.data) is list:
            serializer = DeviceSerializer(data=request.data, many=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(detail=True, methods=['get','post'])
    def logical_partitions(self, request, pk=None):
        if request.method == 'GET':
            data = LogicPartition.objects.filter(device=pk)
            serializer = LogicPartitionSerializer(data, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = LogicPartitionSerializer(data=request.data, many=True)
            if serializer.is_valid(raise_exception=True):
                partitions = serializer.save()
                device = Device.objects.get(pk=pk)
                device.logic_partition.clear()
                for partition in partitions:
                    device.logic_partition.add(partition)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

    @action(detail=True, methods=['get','post'])
    def interfaces(self, request, pk=None):
        if request.method == 'GET':
            data = Interface.objects.filter(device=pk)
            serializer = InterfaceSerializer(data, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            for interface in request.data:
                interface['device'] = pk
            serializer = InterfaceSerializer(data=request.data, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)



class DeviceCommentsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):
    queryset = DeviceComment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeviceChangesViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):
    queryset = Change.objects.all().order_by('updated_at')
    serializer_class = ChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, pk=None):
        fields = Change._meta.get_fields()
        if pk != '-1':
            serializer = ChangeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                change = Change.objects.filter(pk=pk).first()
                for field in fields:
                    setattr(change, field.name, request.data[field.name])
                change.save()
                return Response('200')
            else:
                return Response(serializer.errors)
        else:
            for change in request.data:
                change_obj = Change.objects.filter(id=change['id']).first()
                for field in fields:
                    setattr(change_obj, field.name, change[field.name])
                change_obj.save()
            return Response('200')
    
     
class FutureChangesViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):
    queryset = FutureChange.objects.all()
    serializer_class = FutureChangeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        data = FutureChange.objects.get(id=pk)
        if data.rfc.path and os.path.isfile(data.rfc.path):
            os.remove(data.rfc.path)
        data.delete()
        return Response('200')

    @action(detail=True, methods=['get','post'])
    def downloadFile(self, request, pk=None):
        if request.method == 'GET':
            data = FutureChange.objects.get(id=pk)                            
            wrapper = FileWrapper(open(data.rfc.path, 'rb'))
            response = HttpResponse(wrapper, content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename={}'.format(data.rfc.path)
            return response


class NetworksViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        if type(request.data) is dict:
            serializer = NetworkSerializer(data=request.data)
        elif type(request.data) is list:
            serializer = NetworkSerializer(data=request.data, many=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)