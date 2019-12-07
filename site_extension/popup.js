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



document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("getData").addEventListener("click", getCurrentTabUrl(post_site));
});

chrome.tabs.query({ 'active': true, 'lastFocusedWindow': true, 'currentWindow': true }, function (tabs) {
    var url = tabs[0].url;
    console.log(url);
});

function post_site(url) {

    var xmlhttp = new XMLHttpRequest();
    var apiurl = "http://127.0.0.1:8000/api/v1/create/site";
    xmlhttp.open("POST", apiurl);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    var json_data = JSON.stringify({ "category": "Python", "url": url });
    console.log(json_data);
    try {
        xmlhttp.send(json_data);
    } catch (error) {
        console.log(error);
    }


    // postData(apiurl, json_data)


    // try {
    //     const data = await postData(apiurl, json_data);
    //     console.log(JSON.stringify(data)); // JSON-string from `response.json()` call
    // } catch (error) {
    //     console.error(error);
    // }

};


async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrer: 'no-referrer', // no-referrer, *client
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}