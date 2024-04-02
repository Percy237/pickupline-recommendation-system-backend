from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferred_categories = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "preferred_categories")


class PickupLine(models.Model):
    pickup_line = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.JSONField(default=list)

    def __str__(self):
        return self.pickup_line

    @property
    def category_name(self):
        return self.category.category_name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_line = models.ForeignKey(PickupLine, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
