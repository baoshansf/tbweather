# coding=utf-8


import json
from django.shortcuts import render
from utils.http import ApiResponse
from apps.spider.models import Weather, WeatherDayAverage

#filter out -999, from the tutorial of the filter function. Reference:http://www.cnblogs.com/Lambda721/p/6128424.html
def get_year_data(begin, end, city):
    year_1996 = WeatherDayAverage.objects.filter(
        date__gte=begin,
        date__lte=end,
        city=city, temp__gt=-999
    ).all()

    if len(list(year_1996)) == 0:
        year_1996 = Weather.objects.filter(
            date__gte=begin,
            date__lte=end,
            city=city, temp__gt=-999 , dew_point__gt=-999
        ).all()
    x_value_list = [item.date for item in year_1996]
    temp_list = [str(item.temp) for item in year_1996]
    dew_point_list = [str(item.dew_point) for item in year_1996]
    return x_value_list, temp_list, dew_point_list

# The render statements are rendered using the template of the Django
def web(request):
    if request.method == 'GET':
        return render(request, "show.html")
    elif request.method == "POST":
        param = json.loads(request.body)
        begin_year = int(param.get("begin_date").split("/")[2])
        begin_month = int(param.get("begin_date").split("/")[1])
        begin_day = int(param.get("begin_date").split("/")[0])
        end_year = int(param.get("end_date").split("/")[2])
        end_month = int(param.get("end_date").split("/")[1])
        end_day = int(param.get("end_date").split("/")[0])
        city = param.get("city")
        begin_date = "%s-%.2d-%.2d" % (begin_year, begin_month, begin_day)
        end_date = "%s-%.2d-%.2d" % (end_year, end_month, end_day)
        data = get_year_data(begin_date, end_date, city)
        result = {
            #day-month-year
            "x_value_list": ["/".join(list(reversed(i.split("-")))) for i in data[0] if data[0]] or [0],
            "temp_list": data[1] if data[1] else [0],
            "dew_point_list": data[2] if data[2] else [0],
        }

        return ApiResponse.success(result)
