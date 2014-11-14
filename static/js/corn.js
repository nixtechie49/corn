/**
 * Created by rock on 14-11-14.
 */
$(function () {
    $('input#key_search').quicksearch('ul#keys li');
    var target = $('#hiddenCol').val();
    var db = $('#hiddenDB').val();
    $("#collection").find("option[value=target]").attr("selected", true);
    $('#base').val(db);
    loadDefaultKey();
});

function loadDefaultKey() {
    var target = $('#hiddenCol').val();
    var db = $('#hiddenDB').val();
    getKeys(target, db);
}

function getKeys(target, db) {
    $.ajax({
        type: "GET",
        url: "/collection/",
        data: {target: target, db: db},
        dataType: "json",
        success: function (data) {
            var k = packageKeys(data['keys']);
            $('#keys').empty();   //清空resText里面的所有内容
            $('#keys').html(k);
            var db = data['db'];
            $('#base').val(db);
        }
    });
}

function getValue(key) {
    var target = $('#collection option:selected').val();
    var db = $('#base').val();
    $.ajax({
        type: "POST",
        url: "/value/",
        data: {key: key, col: target, db: db},
        dataType: "text",
        success: function (data) {
            $('#show-value').empty();   //清空resText里面的所有内容
            $('#show-value').html(data);
        }
    });
}

function changeCollection(target) {
    getKeys(target);
}
function changeBase(db) {
    var target = $('#collection option:selected').val();
    getKeys(target, db);
}

function packageKeys(data) {
    html = '';
    for (var i = 0; i < data.length; i++) {
        html += '<li><a href="#" onclick="getValue(\'' + data[i] + '\')">' + data[i] + '</a></li>';
    }
    return html;
}