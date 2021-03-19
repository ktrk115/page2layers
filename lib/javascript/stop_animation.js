setInterval = function(){};
setTimeout = function(){};
var scripts = document.getElementsByTagName('script');
while (scripts.length) {
    var s = scripts[0];
    s.parentNode.removeChild(s);
}