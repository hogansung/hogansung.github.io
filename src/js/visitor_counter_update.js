window.onload = function() {
    var oReq = new XMLHttpRequest();
    oReq.open('get', '/src/php/visitor_counter_update.php', true);
    oReq.send();
}
