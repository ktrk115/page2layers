setInterval = function(){};
setTimeout = function(){};

var scripts = document.getElementsByTagName('script');
while (scripts.length) {
    var s = scripts[0];
    s.parentNode.removeChild(s);
}

var videos = document.getElementsByTagName('video');
for (let i = 0; i < videos.length; i++) {
    videos[i].autoplay = false;
    videos[i].pause();
    videos[i].currentTime = 0;
}