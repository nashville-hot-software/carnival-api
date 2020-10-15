from django.db import models
from django.urls import reverse

class EmployeeType(models.Model):

    name = models.CharField(null=True, max_length=50)

    class Meta:
        verbose_name = ("Employee Type")
        verbose_name_plural = ("Employee Types")


    def __str__(self):
        return f"EmployeeType ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("employee_type_detail", kwargs={"pk": self.pk})