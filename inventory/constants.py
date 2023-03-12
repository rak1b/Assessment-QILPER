from django.db import models
from django.utils.translation import gettext_lazy as _


# PublishChoices  Options
class PublishChoices(models.IntegerChoices):
    DRAFT = 0, _("Draft")
    PUBLISHED = 1, _("Published")
    UNPUBLISHED = 2, _("Unpublished")

class VatType(models.IntegerChoices):
    EXCLUDED = 0, _("Excluded Vat")
    INCLUDED = 1, _("Included Vat")

# Document  Options
