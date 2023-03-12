from ...models import *
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name','phone', 'email', 'website']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'serial_number', ]

class DeligateSerializer(serializers.ModelSerializer):
    company_detail = CompanyListSerializer(source='company', read_only=True)
    employee_detail = EmployeeListSerializer(source='employee', read_only=True)
    device_detail = DeviceListSerializer(source='device', read_only=True,many=True)
    class Meta:
        model = Deligate
        fields = '__all__'
        read_only_fields = ['checked_out', 'returned']


class DeligateListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    device_detail = DeviceListSerializer(source='device', read_only=True,many=True)
    class Meta:
        model = Deligate
        fields = ['id', 'company', 'employee', 'device', 'company_name', 'employee_name', 'device_detail']



class DeviceHistoryListSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    device_condition_display = serializers.CharField(source='get_device_condition_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = DeviceHistory
        fields = ['id', 'device', 'employee', 'device_condition', 'status', 'device_name', 'employee_name', 'device_condition_display', 'status_display']
