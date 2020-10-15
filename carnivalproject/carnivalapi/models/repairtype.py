from django.db import models
from django.urls import reverse

class RepairType(models.Model):

    name = models.CharField(null=True, max_length=50)

    class Meta:
        verbose_name = ("Repair Type")
        verbose_name_plural = ("Repair Types")


    def __str__(self):
        return f"RepairType ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("repair_type_detail", kwargs={"pk": self.pk})
