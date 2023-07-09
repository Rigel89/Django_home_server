from django.contrib import admin

from recipebook.models import Recipe, CookingMode

# Register your models here.

admin.site.register(Recipe)
admin.site.register(CookingMode)