from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    stock = models.IntegerField()
    category = models.CharField()
    is_featured = models.BooleanField(default=False)
