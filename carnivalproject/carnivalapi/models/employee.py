from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .employeetype import EmployeeType
from .dealership import Dealership

class Employee(models.Model):

    first_name = models.CharField(null=True, max_length=20)
    last_name = models.CharField(null=True, max_length=20)
    email_address = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, null=True, help_text='Contact phone number')
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Employee")
        verbose_name_plural = ("Employees")

    def __str__(self):
        return f"Employee ID: {self.pk}"

    def get_absolute_url(self):
        return reverse("employee_detail", kwargs={"pk": self.pk})
