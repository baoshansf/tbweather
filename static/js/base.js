//Base stores the most basic code and other files may use the functions inside
//Code that does not directly relate to the business
//Some of the code comes from looking at other people's blogs and tutorial and rewriting them

function goToUrl(url, newWindow){
    if (newWindow == null){
        newWindow = false;
    }
    if (newWindow == true) {
        window.open(url);
    }
    else{
        window.location.href = url;
    }
}
// Reference:http://www.cnblogs.com/zhaof/p/6281482.html
function AjaxSender(urlStr, methodStr, successFun, errorFun, jsonData) {
    $.ajax({
        url: urlStr,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFTOKEN", $.cookie('csrftoken'));
            xhr.setRequestHeader("auth-token", $.cookie('auth-token'));
        },
        type: methodStr,
        data: jsonData,
        crossDomain: false,
        error: errorFun,
        success: successFun,
        dataType: 'json'
    });
}
// EzajaxGet  is based on Ajaxsender packaging again
// Reference:http://www.cnblogs.com/heihei-haha/p/6211931.html
// The following code is the same

function EzAjaxGet(url, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "get", success, failed);
}

function EzAjaxPut(url, json_param, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "put", success, failed, json_param);
}

function EzAjaxPost(url, json_param, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "post", success, failed, json_param);
}

function EzAjaxDelete(url, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "delete", success, failed);
}

function isNone(obj){
    return obj == "" || obj==null || obj==undefined || obj=={};
}

function getUrlParam(name) {
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}
//customize vue ,cause vue framework's template syntax({{}}) conflicts Django template syntax
var VueData = Vue.extend({
    delimiters: ['${', '}'],
    el: '#vue-div'
});

// Set the date format in the box
// Reference:http://blog.csdn.net/chinet_bridge/article/details/15026729
Date.prototype.Format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //month
        "d+": this.getDate(), //day
        "h+": this.getHours(), //hour
        "m+": this.getMinutes(), //min
        "s+": this.getSeconds(), //second
        "q+": Math.floor((this.getMonth() + 3) / 3), //season
        "S": this.getMilliseconds() //milliseconds
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};

var VueData = Vue.extend({
    delimiters: ['${', '}'],
    el: '#vue-div'
});