from django.db import models
from django.urls import reverse

class PopularVehicle(models.Model):
    
    vehicles_sold = models.IntegerField(null=True)
    body_type = models.CharField(max_length=20, null=True)
    make = models.CharField(max_length=20, null=True)
    model = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = ("Popular Vehicle")
        verbose_name_plural = ("Popular Vehicles")        
        
    def __str__(self):
        return f"Popular Vehicle ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("popular_vehicle_detail", kwargs={"pk": self.pk})