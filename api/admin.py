from django.contrib import admin
from .models import Category, UserCategory, PickupLine, Rating

# Register your models here.
admin.site.register(Category)
admin.site.register(UserCategory)
admin.site.register(PickupLine)
admin.site.register(Rating)
