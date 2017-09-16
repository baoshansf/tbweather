# coding=utf-8
#by myself

from django.contrib import admin
from apps.spider.models import Weather


class WeatherAdmin(admin.ModelAdmin):
    list_display = ('date', 'city', 'time', 'temp', 'dew_point',
                    'humidity', 'pressure', 'visibility',
                    'wind_dir', 'wind_speed', 'conditions')
    list_filter = ('date', 'city', 'time', 'temp', 'dew_point',
                   'humidity', 'pressure', 'visibility',
                   'wind_dir', 'wind_speed', 'conditions')
    list_per_page = 100


admin.site.register(Weather, WeatherAdmin)
