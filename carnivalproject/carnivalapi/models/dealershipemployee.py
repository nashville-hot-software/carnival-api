from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .employee import Employee
from .dealership import Dealership

class DealershipEmployee(models.Model):
    employee_id = models.ForeignKey(employee, related_name="employee", on_delete=models.CASCADE)
    dealership_id = models.ForeignKey(Dealership, related_name="dealership", on_delete=models.CASCADE)



class Meta:

    verbose_name = ("Dealership Employee")
    verbose_name_plural = ("Dealership Employees")

    def __str__(self):
        return f"DealershipEmployee ID: {self.pk}"

    def get_absolute_url(self):
        return reverse("dealership employee_detail", kwargs={"pk": self.pk})
