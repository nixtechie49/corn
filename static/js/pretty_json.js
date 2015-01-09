/**
 * Created by rock on 15-1-9.
 */
function bePretty(j) {
    if (j == undefined || j == null || j.trim() == '') {
        return '';
    }
    try {
        var js = JSON.parse(j);
        if (js instanceof Object || js instanceof Array) {
            return parseNode(js, 0, true);
        } else {
            return j.toString();
        }
    } catch (SyntaxError) {
        return j.toString();
    }
}

function parseNode(js, index, isLast) {
    var isArray = js instanceof Array;
    var s = '';
    if (isArray) {
        s += '[';
    } else {
        s += '{';
    }
    var len = Object.keys(js).length;
    var j = 0;
    for (var i in js) {
        j++;
        s += formatter(index + 1);
        if (js[i] instanceof Array) {
            s += (highlight('"' + i + '":'));
            s += parseNode(js[i], index + 1, j == len);
        } else if (js[i] instanceof Object) {
            if (!isArray) {
                s += highlight('"' + i + '":');
            }
            s += parseNode(js[i], index + 1, j == len);
        } else {
            if (!isArray) {
                s += highlight('"' + i + '":');
            }
            s += highlight('' + js[i] + '', j != len);
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
    var space = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
    var s = '<br>';
    for (var j = 0; j < index; j++) {
        s += space;
    }
    return s;
}

function highlight(match, needComma) {
    var cls = 'green';
    if (/^"/.test(match) && /:$/.test(match)) {
        cls = 'red';
    } else if (/^true|false/.test(match)) {
        cls = 'blue';
    } else if (/null/.test(match)) {
        cls = 'magenta';
    } else if (/^([-]){0,1}([0-9]){1,}([.]){0,1}([0-9]){0,}$/.test(match)) {
        cls = 'darkorange';
    }
    if (cls == 'green') {
        match = '"' + match + '"';
    }
    var s = '<span style="color:' + cls + '">' + match;
    if (needComma && cls != 'red') {
        s += ','
    }
    return s + '</span>';
}