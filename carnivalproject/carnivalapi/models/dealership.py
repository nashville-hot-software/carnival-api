from django.db import models
from django.urls import reverse

class Dealership(models.Model):
    
    business_name = models.CharField(max_length=50, null=False, default="Default Dealership")
    phone = models.CharField(max_length=50, null=False, default="123-456-7891")
    city = models.CharField(max_length=50, null=False, default="Default City")
    state = models.CharField(max_length=50, null=False, default="Default State")
    website = models.CharField(max_length=1000, null=True)
    tax_id = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = ("Dealership")
        verbose_name_plural = ("Dealerships")        
        
    def __str__(self):
        return f"Dealership ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("dealership_detail", kwargs={"pk": self.pk})