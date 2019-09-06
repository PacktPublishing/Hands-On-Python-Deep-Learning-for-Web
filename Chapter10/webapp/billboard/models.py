from django.db import models

from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Bills(models.Model):
    billName = models.CharField("Bill Name", blank=False, max_length=100, default="New Bill")
    user = models.ForeignKey(User, on_delete="CASCADE")
    billDesc = models.TextField("Bill Description")
    billTime = models.DateTimeField(default=now, editable=False)

    class Meta:
        db_table = "bills"