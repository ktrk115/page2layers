const elem = document.querySelector(arguments[0]);
const box = elem.getBoundingClientRect();
return 0 <= box.bottom && box.top <= window.innerHeight