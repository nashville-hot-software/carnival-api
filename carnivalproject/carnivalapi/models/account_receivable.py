from django.db import models
from django.urls import reverse
# from .sale import Sale

class AccountReceivable(models.Model):
    
    credit_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    debit_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    date_received = models.DateField(null=True)
    # sale_id = models.ForeignKey(Sale, related_name="sale", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Account Receivable")
        verbose_name_plural = ("Accounts Receivable")        
        
    def __str__(self):
        return f"Account Receivable ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("account_receivable", kwargs={"pk": self.pk})