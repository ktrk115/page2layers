var elems = document.querySelectorAll("html > head *");
var valid = ["title", "style", "meta", "link", "script", "base"];
for (var i = 0; i < elems.length; i++) {
    var elem = elems[i],
        name = elem.tagName.toLowerCase();
    if (!valid.includes(name)) {
        elem.parentNode.removeChild(elem);
    }
}