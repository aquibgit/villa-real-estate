from django.db import models
from builder_app.models import property_details

# Create your models here.
class booking(models.Model):
    #fields
    user_id=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    property_name=models.CharField(max_length=100)
    property_location=models.CharField(max_length=100)
    property_budget=models.CharField(max_length=100)

class wishlistss(models.Model):
    
    user_id = models.CharField(max_length=100)
    property = models.ForeignKey(property_details, on_delete=models.CASCADE, related_name='wishlisted_entries')
    property_photo = models.ImageField(upload_to='wishlist_photos/', blank=True, null=True)
    property_name = models.CharField(max_length=255)
    property_location = models.CharField(max_length=255)
    property_budget = models.CharField(max_length=100)
    property_bedroom = models.CharField(max_length=100)
    property_bathroom = models.CharField(max_length=100)
    property_area = models.CharField(max_length=100)
    property_floor = models.CharField(max_length=100)
    property_parking = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)