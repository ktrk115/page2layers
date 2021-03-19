const elem = document.querySelector(arguments[0]);
if (!elem || elem.nodeName == 'HTML' || elem.nodeName == '#document-fragment') {
    return true
}

const style = getComputedStyle(elem);
if (style.zIndex != 'auto' && style.position != 'static') {
    return true
}

if (style.position == 'fixed' || style.opacity != '1' ||
    style.transform != 'none' || style.filter != 'none' ||
    style.perspective != 'none' || style.mixBlendMode != 'normal' ||
    style.isolation == 'isolate' || style.willChange == 'transform' ||
    style.willChange == 'opacity' || style.webkitOverflowScrolling == 'touch') {
    return true
}

const pStyle = getComputedStyle(elem.parentElement);
if (style.zIndex != 'auto') {
    if (pStyle.display == 'flex' || pStyle.display == 'inline-flex') {
        return true
    }
}

return false