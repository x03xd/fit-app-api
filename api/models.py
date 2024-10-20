from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    name = models.CharField(max_length=255)

class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meals = models.JSONField() 
    total_calories = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

class Ingredient(models.Model):
    diet_plan = models.ForeignKey(DietPlan, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    grams = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()