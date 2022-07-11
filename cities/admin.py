from django.contrib import admin

from cities.models import City


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ['city_name', 'population', 'type']
