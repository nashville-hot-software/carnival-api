from django.db import models
from django.urls import reverse


class VehicleBodyType(models.Model):

    name = models.CharField(_null=True, max_length=50)

    class Meta:
        verbose_name = ("Vehicle Body Type")
        verbose_name_plural = ("Vehicle Body Types")


    def __str__(self):
        return f"VehicleBodyType ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("vehicle_body_type_detail", kwargs={"pk": self.pk})