function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|BB|PlayBook|IEMobile|Windows Phone|Kindle|Silk|Opera Mini/i.test(
        navigator.userAgent
    )
}

function AJAX(url, params, method='GET', success_callback=function(){}) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open(method, url, true);

    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == XMLHttpRequest.DONE) {
            if (xmlHttp.status == 200) {
                success_callback(xmlHttp.responseText);
            }
            else {
                console.error('AJAX error! Status code:' + xmlHttp.status);
            }
        }
    }

    xmlHttp.send(params);
}