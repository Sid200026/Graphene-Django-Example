from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    continent = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Countries"

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
