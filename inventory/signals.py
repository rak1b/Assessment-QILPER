from django.db.models.signals import pre_save, post_save,m2m_changed
from .models import *
def CreateDevicelog(sender, instance, action, reverse, *args, **kwargs):
  bulkDeviceArray = []
  if action == 'post_add' and not reverse:
    for device in instance.device.all():
        found_device = DeviceHistory.objects.filter(device=device).first()
        if found_device is not None:
          found_device.device_condition = instance.device_status
          found_device.status = instance.deligate_status
          found_device.save()
        else:
          deviceHis = DeviceHistory(device=device,employee=instance.employee,device_condition=instance.device_status,status=instance.deligate_status)
          bulkDeviceArray.append(deviceHis)
  DeviceHistory.objects.bulk_create(bulkDeviceArray)

m2m_changed.connect(CreateDevicelog, sender=Deligate.device.through)