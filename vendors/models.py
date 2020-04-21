from django.db import models

from lib.models import BaseModel


class Vendor(BaseModel):
    name = models.CharField(max_length=2048)
