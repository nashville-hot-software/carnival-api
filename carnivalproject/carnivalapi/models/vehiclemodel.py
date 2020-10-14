from django.db import models
from django.urls import reverse

class VehicleModel(models.Model):
    
    model_name = models.CharField(max_length=20, null=False, default="Default Model Name")

    class Meta:
        verbose_name = ("Vehicle Model")
        verbose_name_plural = ("Vehicle Models")        
        
    def __str__(self):
        return f"Vehicle Model ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("vehicle_model_detail", kwargs={"pk": self.pk})