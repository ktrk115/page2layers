const elem = document.querySelector(arguments[0]);
const style = getComputedStyle(elem, arguments[1]);
return style.content != 'none'