# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    age = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    
class Appliance(models.Model):
    name = models.CharField(max_length=100)
    wattage = models.PositiveIntegerField(help_text="Watts consumed by the appliance")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appliances')

    def __str__(self):
        return self.name

class EnergyUsage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='energy_usage')
    date = models.DateField()
    total_watts_used = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Energy cost in GBP")

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class ApplianceUsage(models.Model):
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE, related_name='usage_entries')
    energy_usage = models.ForeignKey(EnergyUsage, on_delete=models.CASCADE, related_name='appliance_usages')
    watts_used = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.appliance.name} - {self.energy_usage.date}"