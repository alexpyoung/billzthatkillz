from django.db import models

from lib.models import BaseModel
from tags.models import Tag


class Vendor(BaseModel):
    name = models.CharField(max_length=2048)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
