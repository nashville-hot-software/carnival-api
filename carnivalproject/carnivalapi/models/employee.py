from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class employee(models.Model):

    first_name = models.CharField(null=True, max_length=20)


last_name = models.CharField(null=True, max_length=20)
email_address = models.EmailField(max_length=254)
phone = models.PhoneField(null=True, help_text='Contact phone number')
employee_type_id = models.ForeignKey(employee, on_delete=models.CASCADE)
isActive = models.CharField(null=True, max_length=20)
