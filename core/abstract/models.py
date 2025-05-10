from django.db import models
import uuid
from django.shortcuts import get_object_or_404


class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        return get_object_or_404(self.model, public_id=public_id)


class AbstractModel(models.Model):
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AbstractManager()
    
    class Meta:
        abstract = True
    
