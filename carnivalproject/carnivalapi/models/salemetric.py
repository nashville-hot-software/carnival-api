from django.db import models
from django.urls import reverse

class SaleMetric(models.Model):
    
    sale_count = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    class Meta:
        verbose_name = ("Sale Metric")
        verbose_name_plural = ("Sale Metrics")        
        
    def __str__(self):
        return f"Sale Metric ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("sale_metric_detail", kwargs={"pk": self.pk})