from django.db import models
from django.urls import reverse
from .vehiclebodytype import VehicleBodyType
from .vehiclemake import VehicleMake
from .vehiclemodel import VehicleModel

class VehicleType(models.Model):
    
    body_type = models.ForeignKey(VehicleBodyType, related_name="vehicle body type", on_delete = models.CASCADE)
    make = models.ForeignKey(VehicleMake, related_name="vehicle make", on_delete = models.CASCADE)
    model = models.ForeignKey(VehicleModel, related_name="Vehicle Model", on_delete = models.CASCADE)

    class Meta:
        verbose_name = ("Vehicle Type")
        verbose_name_plural = ("Vehicle Types")        
        
    def __str__(self):
        return f"Vehicle Type ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("vehicle_type_detail", kwargs={"pk": self.pk})