/**
 * Created by rock on 15-1-9.
 */
function bePretty(j) {
    if (j === undefined || j === null || trim(j) === '') {
        return '';
    }
    try {
        let js = null;
        if (is.String(j)) {
            js = JSON.parse(j);
        } else {
            js = j;
        }
        if (is.Object(js) || is.Array(js)) {
            return parseNode(js, 0, true);
        } else {
            return j.toString();
        }
    } catch (SyntaxError) {
        return j.toString();
    }
}

function trim(s) {
    if (is.String(s)) {
        s = s.trim()
    }
    return s
}

function parseNode(js, index, isLast) {
    let isArray = is.Array(js);
    let s = '';
    if (isArray) {
        s += '[';
    } else {
        s += '{';
    }
    let len = Object.keys(js).length;
    let j = 0;
    for (let i in js) {
        j++;
        s += formatter(index + 1);
        if (is.Array(js[i])) {
            s += (highlight('"' + i + '":'));
            s += parseNode(js[i], index + 1, j === len);
        } else if (is.Object(js[i])) {
            if (!isArray) {
                s += highlight('"' + i + '":');
            }
            s += parseNode(js[i], index + 1, j === len);
        } else {
            if (!isArray) {
                s += highlight('"' + i + '":');
            }
            s += highlight('' + js[i] + '', j !== len);
        }
    }
    s += formatter(index);
    if (isArray) {
        s += ']';
    } else {
        s += '}';
    }
    if (!isLast) {
        s += ',';
    }
    return s;
}

function formatter(index) {
    let space = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    let s = '<br>';
    for (let j = 0; j < index; j++) {
        s += space;
    }
    return s;
}

function highlight(match, needComma) {
    let cls = 'green';
    if (/^"/.test(match) && /:$/.test(match)) {
        cls = 'red';
    } else if (/^true|false/.test(match)) {
        cls = 'blue';
    } else if (/null/.test(match)) {
        cls = 'magenta';
    } else if (/^([-]){0,1}([0-9]){1,}([.]){0,1}([0-9]){0,}$/.test(match)) {
        cls = 'darkorange';
    }
    if (cls === 'green') {
        match = '"' + match + '"';
    }
    let s = '<span style="color:' + cls + '">' + match;
    if (needComma && cls !== 'red') {
        s += ','
    }
    return s + '</span>';
}

let is = {
    types: ["Array", "Boolean", "Date", "Number", "Object", "RegExp", "String", "Window", "HTMLDocument"]
};
for (let i = 0, c; c = is.types[i++];) {
    is[c] = function (type) {
        return function (obj) {
            return Object.prototype.toString.call(obj) == "[object " + type + "]";
        }
    }(c);
}