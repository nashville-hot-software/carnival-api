from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Customer(models.Model):

    first_name = models.CharField(null=True, max_length=20)
    last_name = models.CharField(null=True, max_length=20)
    email = models.EmailField(max_length=254)
    phone = models.PhoneField(blank=True, help_text='Contact phone number')
    street = models.CharField(null=True, max_length=20)
    city = models.CharField(null=True, max_length=20)
    state = models.CharField(null=True, max_length=20)
    zipcode = models.CharField(null=True, max_length=20)
    company_name = models.CharField(null=True, max_length=20)

    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")

    def __str__(self):
        return f"Customer ID: {self.pk}"

    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"pk": self.pk})
