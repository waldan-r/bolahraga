from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('field_setup', 'Field Setup'),
        ('training_equipment', 'Training Equipment'),
        ('match_equipment', 'Match Equipment'),
        ('safety_recovery', 'Safety & Recovery'),
        ('event_accessories', 'Event Accessories'),
        ('player_gear', 'Player Gear')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name