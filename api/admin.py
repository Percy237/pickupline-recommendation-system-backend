from django.contrib import admin
from .models import Category, PickupLine, Rating, UserProfile

# Register your models here.
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(PickupLine)
admin.site.register(Rating)
