from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    PRESSURE = 'pressure'
    CATEGORY_CHOICES = [
        (TEMPERATURE, 'Temperature Sensor'),
        (HUMIDITY, 'Humidity Sensor'),
        (PRESSURE, 'Pressure Sensor'),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
    
class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    measurement_range = models.CharField(max_length=100)  # Ej: "-40°C to 150°C"
    accuracy = models.CharField(max_length=100)  # Ej: "±0.5°C"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    field_changed = models.CharField(max_length=255)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} changed by {self.changed_by}"
