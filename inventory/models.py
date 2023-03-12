from django.db import models
from . import constants
from datetime import datetime
from coreapp.base import BaseModel
from utility.utils.model_utils import get_code
class Company(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    website = models.URLField()
    notes = models.TextField()

    def __str__(self):
        return self.name

class Employee(BaseModel):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length = 20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Device(BaseModel):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=20, blank=True, null=True)
    device_type = models.SmallIntegerField( choices=constants.DEVICE_TYPE_CHOICES.choices)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    notes = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.serial_number = get_code(Device,"SN",10)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Deligate(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.ManyToManyField(Device)
    checked_out = models.DateTimeField()
    returned = models.DateTimeField()
    device_status = models.SmallIntegerField( choices=constants.DEVICE_TYPE_CHOICES.choices)
    deligate_status = models.SmallIntegerField( choices=constants.DELIGATE_STATUS.choices)

    def save(self, *args, **kwargs):
        if self.returned is None:
            self.returned = datetime.now()
        if self.checked_out is None:
            self.checked_out = datetime.now()
        if self.deligate_status == constants.DELIGATE_STATUS.RETURNED:
            self.returned = datetime.now()
        if self.device_status == constants.DELIGATE_STATUS.CHECKED_OUT:
            self.checked_out = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.company.name}'
    
class DeviceHistory(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True )
    status = models.SmallIntegerField( choices=constants.DELIGATE_STATUS.choices)
    device_condition = models.SmallIntegerField( choices=constants.DEVICE_CONDITION.choices)
    def __str__(self):
        return f'{self.device.name}'