from django.db import models
from django.urls import reverse

class SaleType(models.Model):
    
    name = models.CharField(max_length=8, null=False, default="Purchase")

    class Meta:
        verbose_name = ("Sales Type")
        verbose_name_plural = ("Sales Types")        
        
    def __str__(self):
        return f"Sale Type ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("sale_type_detail", kwargs={"pk": self.pk})