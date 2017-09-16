//By myself
var vue = new VueData({
    data: {
        request: {
            latest_temp_list: "",
            predict_type: ""
        },
        response: {},
        loading: false
    }
});

function search_success(response) {
    if (response.code != 0){
        search_failure();
        return;
    }
    vue.response = response.data;

// This is a visual programming of Echarts.There is a line chart template. Reference: http://echarts.baidu.com/echarts2/doc/example/line1.html

    var base = echarts.init(document.getElementById('chart-div'));
    var option = {
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data: ['the real temperature', 'The predict temperature']
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: vue.response.x_value_list
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name: 'the real temperature',
                type: 'line',
                data: vue.response.real_temp_list,
                markLine: {
                    data: [
                        {type: 'average', name: 'average temperature'}
                    ]
                }
            },
            {
                name: 'The predict temperature',
                type: 'line',
                data: vue.response.predict_temp_list,
                markLine: {
                    data: [
                        {type: 'average', name: 'average temperature'}
                    ]
                }
            }
        ]
    };
    base.setOption(option);

    vue.loading = false;
}

function search_failure(){
    vue.loading = false;
    $.alert({
        title: 'Error',
        content: "System Error",
        confirmButton: 'Ok'
    });
}

function click_search() {
    if(isNone(vue.request.latest_temp_list) || isNone(vue.request.predict_type)){
        $.alert({
            title: 'Warning',
            content: "Params can not be null",
            confirmButton: 'Ok'
        });
        return;
    }
    var json = JSON.stringify(vue.request);
    vue.loading = true;
    EzAjaxPost(ApiUri.mining, json, search_success, search_failure);
}