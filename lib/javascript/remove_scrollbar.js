const _head = document.head || document.getElementsByTagName('head')[0];
const _sheet = document.createElement('style');
_sheet.innerHTML = '::-webkit-scrollbar {display: none;}';
_head.appendChild(_sheet);