from django.db import models
from django.urls import reverse
from .vehicle import Vehicle

class OilChangeLog(models.Model):
    
    vehicle = models.ForeignKey(Vehicle, related_name="vehicle", on_delete=models.CASCADE)
    oil_change_date = models.DateField(null=False, default="2000-01-01")

    class Meta:
        verbose_name = ("Oil Change")
        verbose_name_plural = ("Oil Changes")        
        
    def __str__(self):
        return f"Oil Change ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("oil_change_detail", kwargs={"pk": self.pk})