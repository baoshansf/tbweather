# coding=utf-8


from apps.spider.models import Weather
import requests

from bs4 import BeautifulSoup
import datetime
import time
import random
from tbweather.settings import WEATHER_CITY


def date_list(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)
    result = []
    curr_date = start_date
    while curr_date != end_date:
        #  The front-end echarts display requires converting float data into strings
        #  My friend helped me debug
        result.append(("%04d" % curr_date.year, "%02d" % curr_date.month, "%02d" % curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append(("%04d" % curr_date.year, "%02d" % curr_date.month, "%02d" % curr_date.day))
    return result

#by myself

def grasp_weather(year, month, day, city):
    url = WEATHER_CITY[city].format(year, month, day)
    html_content = requests.get(url).content
    b = BeautifulSoup(html_content, "html.parser")
    table = b.find("table", {"id": "obsTable"}).find_all("tr", {"class": "no-metars"})
    item_count = 0
    for i in table:
        a = []
        for j in i.find_all("td"):
            a.append(j.text.replace("\r", "").replace("\n", ""))
        try:
            time = a[0]
            if "AM" in time:
                hour = int(time.split()[0].split(":")[0])
                minute = int(time.split()[0].split(":")[1])
                if hour == 12:
                    time = "%02d:%02d:00" % (0, minute)
                else:
                    time = "%02d:%02d:00" % (hour, minute)
            elif "PM" in time:
                hour = int(time.split()[0].split(":")[0])
                minute = int(time.split()[0].split(":")[1])
                if hour == 12:
                    time = "%02d:%02d:00" % (hour, minute)
                else:
                    time = "%02d:%02d:00" % (hour + 12, minute)
        except:
            time = "-"
        try:
            temp = float(a[1].split()[0])
        except:
            temp = float(-999)
        try:
            dew_point = float(a[2].split()[0])
        except:
            dew_point = float(-999)
        try:
            humidity = float(a[3][:-1])/100.0
        except:
            humidity = float(-999)
        try:
            pressure = int(a[4].split()[0])
        except:
            pressure = float(-999)
        try:
            visibility = float(a[5].split()[0])
        except:
            visibility = float(-999)
        try:
            wind_dir = a[6]
        except:
            wind_dir = "-"
        try:
            wind_speed = float(a[7].split()[0])
        except:
            wind_speed = float(-999)
        try:
            conditions = a[-1]
        except:
            conditions = "-"
        weather = Weather(
            city=city,
            date=str("%s-%s-%s" % (year, month, day)),
            time=time,
            temp=temp,
            dew_point=dew_point,
            humidity=humidity,
            pressure=pressure,
            visibility=visibility,
            wind_dir=wind_dir,
            wind_speed=wind_speed,
            conditions=conditions
        )
        weather.save()
        item_count += 1

    return item_count


def grasp_weather_range(begin, end, city):
    """
    :param begin: tuple like (2016, 1,1)
    :param end: tuple like (2017, 1,1)
    :param city: city like Cardiff
    :return:
    """
    dates = date_list(begin, end)
    total_count = 0
    for year, month, day in dates:
        try:
            total_count += grasp_weather(year, month, day, city)
        except Exception, e:
            print year, month, day, e
         #  Set climbing interval
        time.sleep(random.randint(2, 15))
    return len(dates), total_count
