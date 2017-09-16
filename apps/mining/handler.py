# coding=utf-8


from apps.spider.models import WeatherDayAverageTemp
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model

def predict_by_similarity_mine(temp_list):
    """
    own similarity algorithm
    The temperature of the next day is predicted by the similarity of the temperature
    :param: temp_list  list of temperatures a few days ago
    :return: return forecast temperature
    """
    # Historical data, which removes data from 2017, is used as a regression test
    history_temp_list = [item.temp for item in WeatherDayAverageTemp.objects.filter(date__lt="2017")]
    # The similarity list stores all the similarity values
    similar_list = []
    # Sequential traversal
    for i in xrange(0, len(history_temp_list) - len(temp_list)):
        # Take out a string of weather data which is the same as the size of temp_list
        history = history_temp_list[i:len(temp_list) + i]
        delta_list = []
        # Compute similarity
        for j in range(len(temp_list)):
            delta_list.append(1 - (abs(temp_list[j] - history[j])/max(history_temp_list)))
        #Seek help from friend
        #The results I need: to calculate the similarity between the 2 temperatures, reduce is to calculate the product of each similarity, that is, the similarity of the total sequence
        similar_value = reduce(lambda x, y: x * y, delta_list)
        similar_list.append(similar_value)
    # Find the maximum similarity index. The index must correspond to the index of the first number of the historical data
    max_value_index = similar_list.index(max(similar_list))
    # Take out the list of data with the largest similarity and take one more. This one is the predicted data
    max_pare_list = history_temp_list[max_value_index:max_value_index + len(temp_list) + 1]
    return ",".join([str(i) for i in max_pare_list]), max_pare_list[-1]


def predict_by_similarity(temp_list):
    """
    Pearson
    The temperature of the next day is predicted by the similarity of the temperature
    :param: temp_list  list of temperatures a few days ago
    :return: return forecast temperature
    """
    # Historical data were removed from 2017 data, and the year's data were used as regression tests
    history_temp_list = [item.temp for item in WeatherDayAverageTemp.objects.filter(date__lt="2017")]
    # The similarity list stores all the similarity values
    similar_list = []
    average = sum(history_temp_list) / len(history_temp_list)
    for i in xrange(0, len(history_temp_list) - len(temp_list)):
        # Take out a string of weather data which is the same as the size of temp_list
        history = history_temp_list[i:len(temp_list) + i]
        # Compute similarity
        Numerator = 0
        Denominator = 1
        for j in range(len(temp_list)):
            #formula
            Numerator += (temp_list[j] - average) * (history[j] - average)
            Denominator *= ((temp_list[j] - average) ** 2 + (history[j] - average) ** 2) ** 0.5
        similar_value = Numerator / float(Denominator)
        similar_list.append(similar_value)
    # Find the maximum similarity index. The index must correspond to the index of the first number of the historical data
    max_value_index = similar_list.index(max(similar_list))
    # Take out the list of data with the largest similarity and take one more. This one is the predicted data
    max_pare_list = history_temp_list[max_value_index:max_value_index + len(temp_list) + 1]
    return ",".join([str(i) for i in max_pare_list]), max_pare_list[-1]


# -------------------linear_regression----------------------------------------
def get_parameters():
    #filter 2017
    history_data = [item.temp for item in WeatherDayAverageTemp.objects.filter(date__lt="2017").all()]
    x_parameters = []
    y_parameters = []
    compare_len = 1
    #formula
    for i in xrange(len(history_data)):
        x_item = sum(history_data[i:i+compare_len]) / float(compare_len)
        if i + compare_len + 1 < len(history_data):
            x_parameters.append([x_item])
            y_parameters.append(history_data[i + compare_len])
    return x_parameters, y_parameters

    # y=ax+b
def predict_by_linear_regression(x_parameters, y_parameters, predict_value):
    regr = linear_model.LinearRegression()
    regr.fit(x_parameters, y_parameters)
    predict_outcome = regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
    return predictions

   #draw linear using maplotlib
def show_linear_line(x_parameters, y_parameters):
    regr = linear_model.LinearRegression()
    regr.fit(x_parameters, y_parameters)
    plt.scatter(x_parameters, y_parameters, color='blue')
    plt.plot(x_parameters, regr.predict(x_parameters), color='red', linewidth=4)
    plt.xticks(())
    plt.yticks(())
    plt.show()
