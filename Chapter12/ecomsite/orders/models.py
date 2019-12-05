from django.db import models

# Create your models here.
class Order (models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    product_id = models.IntegerField()
    amount = models.IntegerField()
    order_status = models.CharField(max_length=20, default="Confirmed")