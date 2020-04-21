import re
import uuid

from django.db import models
from money import Money


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=2048)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=8)

    @classmethod
    def sanitize(cls, date, vendor_name, cost):
        amount = Money(amount=cost, currency="USD")
        (vendor, __) = Vendor.objects.get_or_create(
            # Strip digits for better coalescing
            name=re.sub(r"([0-9]+)", "", vendor_name.strip()),
        )
        return cls(
            date=date,
            vendor=vendor,
            amount=amount.amount,
            currency=amount.currency,
        )
