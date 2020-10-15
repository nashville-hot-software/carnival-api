from django.db import models
from django.urls import reverse

class VehicleMake(models.Model):

    name = models.CharField(null=True, max_length=50)

    class Meta:
        verbose_name = ("Vehicle Make")
        verbose_name_plural = ("Vehicle Makes")


    def __str__(self):
        return f"VehicleMake ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("vehicle_make_detail", kwargs={"pk": self.pk})