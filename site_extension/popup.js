// http://127.0.0.1:8000/api/v1/list/categories

// http://127.0.0.1:8000/api/v1/list/categories

// document.getElementById("getData").addEventListener("click");


function getCurrentTabUrl(callback) {
    var queryInfo = {
        active: true,
        currentWindow: true
    };

    chrome.tabs.query(queryInfo, function (tabs) {
        var tab = tabs[0];
        var url = tab.url;
        console.assert(typeof url == 'string', 'tab.url should be a string');
        console.log(url);
        callback(url);
    });
}

function getProduct(url, callback, errorCallback) {
    if (url.indexOf('verkkokauppa.com/') != -1 && url.indexOf('/product/') != -1) {
        var productCode = url.split('product/')[1].split('/')[0];
        var searchUrl = 'https://bloodhound.me/api/product/' +
            '?code=' + encodeURIComponent(productCode);

        var x = new XMLHttpRequest();
        x.open('GET', searchUrl);

        x.onload = function () {
            var response = x.response;
            callback(response);
        };

        x.onerror = function () {
            errorCallback('Network error.');
        };

        x.send();
    }
    else {
        errorCallback('No product found in this page.');
        return;
    }
}

function renderStatus(statusText) {
    document.getElementById('main').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("getData").addEventListener("click", getCurrentTabUrl(post_site));
});

function post_site(url) {

    var xmlhttp = new XMLHttpRequest();
    var apiurl = "http://127.0.0.1:8000/api/v1/create/site";
    xmlhttp.open("POST", apiurl);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    var json_data = JSON.stringify({ "category": "Python", "url": url });
    console.log(json_data);
    xmlhttp.send(json_data);

};

