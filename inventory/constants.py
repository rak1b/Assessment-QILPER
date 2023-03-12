from django.db import models
from django.utils.translation import gettext_lazy as _
class DEVICE_TYPE_CHOICES(models.IntegerChoices):
    ELECTRONIC = 0, _("Electronic")
    HARDWARE = 1, _("Hardware")
    SOFTWARE = 2, _("Software")
    OTHER = 3, _("Other")


class DELIGATE_STATUS(models.IntegerChoices):
    CHECKED_OUT = 0, _("Checked Out")
    RETURNED = 1, _("Returned")

class DEVICE_CONDITION(models.IntegerChoices):
    WORKING = 0, _("Working")
    NOT_WORKING = 1, _("Not Working")
    OTHER = 2, _("Other")
