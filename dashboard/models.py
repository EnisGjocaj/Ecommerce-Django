from django.db import models
from django.contrib.auth.models import User
from item.models import Item

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f"Cart for {self.user.username}"