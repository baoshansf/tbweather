# coding=utf-8

#by myself
from django.db import models


class Weather(models.Model):
    city = models.CharField(max_length=100, default="Cardiff", verbose_name=u"City")
    date = models.CharField(max_length=10, verbose_name=u"date")
    time = models.CharField(max_length=10, verbose_name=u"time")
    temp = models.FloatField(verbose_name=u"temperature")
    dew_point = models.FloatField(verbose_name=u"dew")
    humidity = models.FloatField(verbose_name=u"humidity")
    pressure = models.IntegerField(verbose_name=u"pressure")
    visibility = models.FloatField(verbose_name=u"visibility")
    wind_dir = models.CharField(max_length=30, verbose_name=u"wind-dir")
    wind_speed = models.FloatField(verbose_name=u"wind-speed")
    conditions = models.CharField(max_length=30, verbose_name=u"condition")

    class Meta:
        db_table = 'Weather'
        verbose_name = u'data'
        verbose_name_plural = u'data'


class WeatherDayAverage(models.Model):
    city = models.CharField(max_length=100, default="Cardiff", verbose_name=u"City")
    date = models.CharField(max_length=10, verbose_name=u"Date")
    temp = models.FloatField(verbose_name=u"Temperature")
    dew_point = models.FloatField(verbose_name=u"Dew")
    humidity = models.FloatField(verbose_name=u"humidity")
    pressure = models.IntegerField(verbose_name=u"pressure")
    visibility = models.FloatField(verbose_name=u"visibility")

    class Meta:
        db_table = 'WeatherDayAverage'
        verbose_name = u'day-ave'
        verbose_name_plural = u'day-ave'


class WeatherDayAverageTemp(models.Model):
    city = models.CharField(max_length=100, default="Cardiff", verbose_name=u"City")
    date = models.CharField(max_length=10, verbose_name=u"date")
    temp = models.FloatField(verbose_name=u"temperature")

    class Meta:
        db_table = 'WeatherDayAverageTemp'
        verbose_name = u'day-avetem'
        verbose_name_plural = u'day-avetemp'


class WeatherDayAverageTempDewPoint(models.Model):
    city = models.CharField(max_length=100, default="Cardiff", verbose_name=u"City")
    date = models.CharField(max_length=10, verbose_name=u"date")
    temp = models.FloatField(verbose_name=u"temperature")
    dew_point = models.FloatField(verbose_name=u"dew")

    class Meta:
        db_table = 'WeatherDayAverageTempDewPoint'
        verbose_name = u'DayAverageTempDewPoint'
        verbose_name_plural = u'DayAverageTempDewPoint'

