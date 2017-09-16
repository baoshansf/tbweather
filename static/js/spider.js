//by myself
var vue = new VueData({
    data: {
        request: {
            begin_date: "",
            end_date: "",
            city: ""
        },
        response: "",
        loading: false
    }
});

function search_success(response) {
    if (response.code != 0){
        search_failure();
        return;
    }
    vue.response = response.data;
    
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
    if(isNone(vue.request.begin_date) || isNone(vue.request.end_date)
       || isNone(vue.request.city)){
        $.alert({
            title: 'Warning',
            content: "Param can not be null",
            confirmButton: 'Ok'
        });
        return;
    }
    var json = JSON.stringify(vue.request);
    vue.loading = true;
    EzAjaxPost(ApiUri.spider, json, search_success, search_failure);
}

//Add calendar Reference: http://bootstrap-datepicker.readthedocs.io/en/latest/
// Set the date format for datepicker from tutorial in Chinese Reference: http://blog.csdn.net/gulingeagle/article/

$("#begin-date").datepicker({ dateFormat: 'dd/mm/yy' });
$("#end-date").datepicker({ dateFormat: 'dd/mm/yy' });