var httpRequest = new XMLHttpRequest();

httpRequest.onload = function() {  

    if (httpRequest.readyState == 4 && httpRequest.status == 200) {

        document.getElementById('debug').innerHTML =
            httpRequest.response;  }

    return; }

httpRequest.open('post', 'debug.txt', true);
httpRequest.send();
