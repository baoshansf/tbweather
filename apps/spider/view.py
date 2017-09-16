# coding=utf-8
# by myself

from django.shortcuts import render
import json
from apps.spider.handler import grasp_weather_range
from utils.http import ApiResponse


def spider(request):
    if request.method == "GET":
        return render(request, "spider.html")
    elif request.method == "POST":
        try:
            param = json.loads(request.body)
            begin_year = int(param.get("begin_date").split("/")[2])
            begin_month = int(param.get("begin_date").split("/")[1])
            begin_day = int(param.get("begin_date").split("/")[0])
            end_year = int(param.get("end_date").split("/")[2])
            end_month = int(param.get("end_date").split("/")[1])
            end_day = int(param.get("end_date").split("/")[0])
            city = param.get("city")
            result = grasp_weather_range((begin_year, begin_month, begin_day), (end_year, end_month, end_day), city)
            data = {
                "days": result[0],
                "items": result[1]
            }
            return ApiResponse.success(data)
        except Exception, e:
            print e
            return ApiResponse.failure(-1, str(e))
