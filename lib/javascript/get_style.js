const out = {};
const elem = document.querySelector(arguments[0]);
const keys = arguments[1];
const style = getComputedStyle(elem, arguments[2]);
for (let i = 0; i < keys.length; i++) {
    let key = keys[i];
    { out[key] = style[key] };
}
return out