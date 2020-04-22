import re

from django.db import models
from money import Money

from lib.models import BaseModel
from tags.models import Tag
from vendors.models import Vendor


class Purchase(BaseModel):
    date = models.DateTimeField()
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=8)
    name = models.CharField(max_length=2048)
    tags = models.ManyToManyField(Tag)

    @classmethod
    def sanitize(cls, date, vendor_name, cost):
        amount = Money(amount=cost, currency="USD")
        (vendor, __) = Vendor.objects.get_or_create(
            # Strip digits for better coalescing
            name=re.sub(r"([0-9]+)", "", vendor_name.strip()),
        )
        return cls(
            date=date,
            name=vendor_name,
            vendor=vendor,
            amount=amount.amount,
            currency=amount.currency,
        )
