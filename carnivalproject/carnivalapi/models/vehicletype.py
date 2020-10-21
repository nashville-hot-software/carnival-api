from django.db import models
from django.urls import reverse

class VehicleType(models.Model):
    
    body_type = models.CharField(max_length=20, null=True)
    make = models.CharField(max_length=20, null=True)
    model = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = ("Vehicle Type")
        verbose_name_plural = ("Vehicle Types")        
        
    def __str__(self):
        return f"Vehicle Type ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("vehicle_type_detail", kwargs={"pk": self.pk})