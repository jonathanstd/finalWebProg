from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    profile_picture = models.ImageField(upload_to='profile_images/')
    # Other user-related fields

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    # Other document-related fields

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
