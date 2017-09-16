# coding=utf-8


from django.shortcuts import render
import json
from utils.http import ApiResponse
from apps.mining.handler import predict_by_similarity, predict_by_similarity_mine
from apps.spider.handler import date_list
from apps.spider.models import WeatherDayAverageTemp


def mining(request):
    if request.method == "GET":
        return render(request, "mining.html")

    elif request.method == "POST":
        param = json.loads(request.body)
        latest_temp_list = [float(item) for item in param.get("latest_temp_list").split(",")]
        predict_type = param.get("predict_type", "similarity")
        # time interval for comparsion
        dl = ["%s-%s-%s" % item for item in date_list((2017, 1, 1), (2017, 5, 1))]
        predict_len = 3
        # Comparing [n-3] similarity Reference:https://stackoverflow.com/questions/5245307/django-date-filter-gte-and-lte
        real_temp_list = [item.temp for item in
                          WeatherDayAverageTemp.objects.filter(date__gte=dl[0], date__lte=dl[-1]).all()]
        # Choose algorithm
        if predict_type == "Similarity":
            history_1, predict_result_1 = predict_by_similarity(latest_temp_list)
            latest_temp_list.append(predict_result_1)
            history_2, predict_result_2 = predict_by_similarity(latest_temp_list)
            latest_temp_list.append(predict_result_2)
            history_3, predict_result_3 = predict_by_similarity(latest_temp_list)
            latest_temp_list.append(predict_result_3)
            history_4, predict_result_4 = predict_by_similarity(latest_temp_list)
            latest_temp_list.append(predict_result_4)
            history_5, predict_result_5 = predict_by_similarity(latest_temp_list)
            #seek help ,the result I want is predicted temperature list generator
            predict_temp_list = [predict_by_similarity(real_temp_list[index:index+predict_len])[1] for index in xrange(len(real_temp_list))]

            data = {
                "predict_result": "%s,%s,%s,%s,%s" % (predict_result_1, predict_result_2, predict_result_3,
                                                      predict_result_4, predict_result_5),
                "history": history_1,
                "real_temp_list": real_temp_list[predict_len:-1],
                "predict_temp_list": predict_temp_list[:-1],
                "x_value_list": dl[predict_len:-1]
            }
            return ApiResponse.success(data)
        elif predict_type == "SimilarityMine":
            history_1, predict_result_1 = predict_by_similarity_mine(latest_temp_list)
            latest_temp_list.append(predict_result_1)
            history_2, predict_result_2 = predict_by_similarity_mine(latest_temp_list)
            latest_temp_list.append(predict_result_2)
            history_3, predict_result_3 = predict_by_similarity_mine(latest_temp_list)
            latest_temp_list.append(predict_result_3)
            history_4, predict_result_4 = predict_by_similarity_mine(latest_temp_list)
            latest_temp_list.append(predict_result_4)
            history_5, predict_result_5 = predict_by_similarity_mine(latest_temp_list)
            predict_temp_list = [predict_by_similarity_mine(real_temp_list[index:index+predict_len])[1] for index in xrange(len(real_temp_list))]
            data = {
                "predict_result": "%s,%s,%s,%s,%s" % (predict_result_1, predict_result_2, predict_result_3,
                                                      predict_result_4, predict_result_5),
                "history": history_1,
                "real_temp_list": real_temp_list[predict_len:-1],
                "predict_temp_list": predict_temp_list[:-1],
                "x_value_list": dl[predict_len:-1]
            }
            return ApiResponse.success(data)
        elif predict_type == "Linear regression":
            from apps.mining.handler import get_parameters, predict_by_linear_regression, show_linear_line
            # The average temperature of the next day is calculated sequentially, and then the predicted temperature is obtained
            x_list, y_list = get_parameters()
            avg_latest = sum(latest_temp_list) / float(len(latest_temp_list))
            result_1 = predict_by_linear_regression(x_list, y_list, avg_latest)
            latest_temp_list.append(result_1['predicted_value'][0])
            avg_latest = sum(latest_temp_list) / float(len(latest_temp_list))
            result_2 = predict_by_linear_regression(x_list, y_list, avg_latest)
            latest_temp_list.append(result_2['predicted_value'][0])
            avg_latest = sum(latest_temp_list) / float(len(latest_temp_list))
            result_3 = predict_by_linear_regression(x_list, y_list, avg_latest)
            latest_temp_list.append(result_3['predicted_value'][0])
            avg_latest = sum(latest_temp_list) / float(len(latest_temp_list))
            result_4 = predict_by_linear_regression(x_list, y_list, avg_latest)
            latest_temp_list.append(result_4['predicted_value'][0])
            avg_latest = sum(latest_temp_list) / float(len(latest_temp_list))
            result_5 = predict_by_linear_regression(x_list, y_list, avg_latest)
            #generate temperature list
            predict_temp_list = [
                predict_by_linear_regression(x_list, y_list, sum(real_temp_list[index:index+predict_len])/float(predict_len))['predicted_value'][0]
                for index in xrange(len(real_temp_list))]
            data = {
                "predict_result": "%s,%s,%s,%s,%s" % (result_1['predicted_value'][0], result_2['predicted_value'][0],
                                                      result_3['predicted_value'][0], result_4['predicted_value'][0],
                                                      result_5['predicted_value'][0]),
                "history": "None",
                "real_temp_list": real_temp_list[predict_len:-1],
                "predict_temp_list": predict_temp_list[:-1],
                "x_value_list": dl[predict_len:-1]
            }
            # show_linear_line(x_list, y_list)
            return ApiResponse.success(data)






