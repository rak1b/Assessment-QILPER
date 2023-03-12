
from . import serializers
from ...models import *
from coreapp.helper import *

class CompanyAPI(ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = Company.objects.all().order_by('-created_at')
  serializer_class = serializers.CompanySerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  filterset_fields = ['name', 'phone', 'email', 'website']
  search_fields = ['name', 'email', 'website']

  def get_serializer_class(self):
    if self.action == 'list':
      return serializers.CompanyListSerializer
    return serializers.CompanySerializer
  
class EmployeeAPI(ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = Employee.objects.all().order_by('-created_at')
  serializer_class = serializers.EmployeeSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  filterset_fields = ['company','email', 'phone']
  search_fields = ['first_name', 'last_name', 'email', 'phone']

  def get_serializer_class(self):
    if self.action == 'list':
      return serializers.EmployeeListSerializer
    return serializers.EmployeeSerializer
  
class DeviceAPI(ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = Device.objects.all().order_by('-created_at')
  serializer_class = serializers.DeviceSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  filterset_fields = ['name', 'serial_number', 'device_type']
  search_fields = ['name', 'serial_number', 'device_type']

  def get_serializer_class(self):
    if self.action == 'list':
      return serializers.DeviceListSerializer
    return serializers.DeviceSerializer
  
class DeligateAPI(ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = Deligate.objects.all().order_by('-created_at')
  serializer_class = serializers.DeligateSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  filterset_fields = ['company__name', 'employee__first_name', 'device__name']
  search_fields =  ['company__name', 'employee__first_name', 'device__name']

  def get_serializer_class(self):
    if self.action == 'list':
      return serializers.DeligateListSerializer
    return serializers.DeligateSerializer
  
class DeviceHistoryAPI(ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = DeviceHistory.objects.all().order_by('-created_at')
  serializer_class = serializers.DeviceHistoryListSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
  filterset_fields = ['device__name', 'employee__first_name', 'device_condition', 'status']
  search_fields = ['device__name', 'employee__first_name', 'device_condition', 'status']
  http_method_names = ['get']
