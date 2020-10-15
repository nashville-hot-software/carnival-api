from django.db import models
from django.urls import reverse
from .vehicletype import VehicleType

class Vehicle(models.Model):
    
    vin = models.CharField(max_length=50, null=False, default="AAAAAAAAAAAAAAA")
    engine_type = models.CharField(max_length=2, null=False, default="V6")
    vehicle_type = models.ForeignKey(VehicleType, related_name="vehicle type", on_delete=models.CASCADE)
    exterior_color = models.CharField(max_length=50, null=False, default="Default Exterior Color")
    interior_color = models.CharField(max_length=50, null=False, default="Default Interior Color")
    floor_price = models.IntegerField(null=False, default=20000)
    msr_price = models.IntegerField(null=False, default=15000)
    miles_count = models.IntegerField(null=False, default=100)
    year_of_car = models.IntegerField(null=False, default=2020)
    is_sold = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name = ("Vehicle")
        verbose_name_plural = ("Vehicles")        
        
    def __str__(self):
        return f"Vehicle ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("vehicle_detail", kwargs={"pk": self.pk})