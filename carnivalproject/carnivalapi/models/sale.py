from django.db import models
from django.urls import reverse
# from .saletype import SaleType
# from .vehicle import Vehicle

class Sale(models.Model):
    
    # sales_type = models.ForeignKey(SaleType, related_name="saletype", on_delete = models.CASCADE)
    # vehicle = models.ForeignKey(Vehicle, related_name="vehicle", on_delete = models.CASCADE)
    # employee = models.ForeignKey(Employee, related_name="employee", on_delete = models.CASCADE)
    # customer = models.ForeignKey(Customer, related_name="customer", on_delete = models.CASCADE)
    # dealership = models.ForeignKey(Dealership, related_name="dealership", on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, default=1000)
    deposit = models.IntegerField(null=False, default=1000)
    purchase_date = models.DateField(null=False, default='2000-01-01')
    pickup_date = models.DateField(null=False, default='2000-01-01')
    invoice_number = models.CharField(null=False, max_length=50, default='1111111111')
    payment_method = models.CharField(null=False, max_length=50, default='visa')
    returned = models.BooleanField(null=False, default='false')


    class Meta:
        verbose_name = ("Sale")
        verbose_name_plural = ("Sales")        
        
    def __str__(self):
        return f"Sale ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("sale_detail", kwargs={"pk": self.pk})