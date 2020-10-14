from django.db import models
from django.urls import reverse
from .repairtype import RepairType
from .vehicle import Vehicle
class CarRepairType(models.Model):

    name = models.CharField(_null=True, max_length=50)
    date_occured = models.DateTimeField(auto_now=True)
    vehicle_id = models.ForeignKey(Vehicle, related_name="vehicle", on_delete = models.CASCADE)
    repair_type_id = models.ForeignKey(RepairType, related_name="repairtype", on_delete = models.CASCADE)
    class Meta:
        verbose_name = ("Car Repair Type")
        verbose_name_plural = ("Car Repair Types")


    def __str__(self):
        return f"CarRepairType ID: {self.pk}"
    
    def get_absolute_url(self):
        return reverse("car_repair_type_detail", kwargs={"pk": self.pk})
