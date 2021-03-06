from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .employee import Employee
from .dealership import Dealership

class DealershipEmployee(models.Model):

    employee = models.ForeignKey(Employee, related_name="dealershipemployee", on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, related_name="employeedealership", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Dealership Employee")
        verbose_name_plural = ("Dealership Employees")

    def __str__(self):
        return f"DealershipEmployee ID: {self.pk}"

    def get_absolute_url(self):
        return reverse("dealership employee_detail", kwargs={"pk": self.pk})
