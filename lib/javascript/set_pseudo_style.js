const _sheetId = 'pseudoStyles';
const _head = document.head || document.getElementsByTagName('head')[0];
const _sheet = document.getElementById(_sheetId) || document.createElement('style');
_sheet.id = _sheetId;

const elem = document.querySelector(arguments[0]);
const cssText = arguments[1];
const className = arguments[2];

elem.className += ' ' + className;
_sheet.innerHTML += ' .' + className + arguments[3] + ' {' + cssText + '}';
_head.appendChild(_sheet);