// by myself
var vue = new VueData({
    data: {
        request: {
            begin_date: "11-01",
            end_date: "12-01",
            city: ""
        },
        response: {
            x_value_list: [],
            temp_list: [],
            dew_point_list: []
        },
        loading: false
    }
});

function search_success(response) {
    if (response.code != 0){
        search_failure();
        return;
    }
// // This is a visual programming of Echarts.There is a line chart template. Reference: http://echarts.baidu.com/echarts2/doc/example/line1.html
    var item = response.data;
    var base = echarts.init(document.getElementById('chart-show'));
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
            data: ['Temperature', 'Dew Point']
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: item.x_value_list
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
                name: 'Temperature',
                type: 'line',
                data: item.temp_list,
                markLine: {
                    data: [
                        {type: 'average', name: 'average'}
                    ]
                }
            },
            {
                name: 'Dew Point',
                type: 'line',
                data: item.dew_point_list,
                markLine: {
                    data: [
                        {type: 'average', name: 'average'}
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
        content: "System error",
        confirmButton: 'Ok'
    });
}

function click_search() {
    vue.request.begin_date = $("#begin-date").val();
    vue.request.end_date = $("#end-date").val();
    if(isNone(vue.request.begin_date) || isNone(vue.request.end_date) || isNone(vue.request.city)){
        $.alert({
            title: 'Warning',
            content: "Params can not be null",
            confirmButton: 'Ok'
        });
        return;
    }
    var json = JSON.stringify(vue.request);
    vue.loading = true;
    EzAjaxPost(ApiUri.show, json, search_success, search_failure);
}
//Add calendar Reference: http://bootstrap-datepicker.readthedocs.io/en/latest/
// Set the date format for datepicker from tutorial in Chinese Reference: http://blog.csdn.net/gulingeagle/article/details/43567101

$("#begin-date").datepicker({ dateFormat: 'dd/mm/yy' });
$("#end-date").datepicker({ dateFormat: 'dd/mm/yy' });