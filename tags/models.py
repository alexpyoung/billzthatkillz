from django.db import models

from lib.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=2048)

    def __str__(self):
        return self.name
