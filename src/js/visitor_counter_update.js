window.onload = function() {
    var oReq = new XMLHttpRequest();
    oReq.open('get', '/php/visitor_counter_update.php', true);
    oReq.send();
}
