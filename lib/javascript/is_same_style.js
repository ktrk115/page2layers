const elem = document.querySelector(arguments[0]);
const target = arguments[1];
const style = getComputedStyle(elem, arguments[2]);
for (let key in target) {
    if (style[key] != target[key]) { return false };
}
return true