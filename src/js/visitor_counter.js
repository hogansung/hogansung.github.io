function reqListener () {
    console.log(this.responseText);
}

window.onload = function() {
    var oReq = new XMLHttpRequest();
    oReq.onload = function() {
        var total_number_visit = JSON.parse(this.responseText);
        for (i = 0; i < 6; i++) {
            document.getElementById('d' + i).innerHTML = total_number_visit % 10;
            total_number_visit = Math.floor(total_number_visit / 10);
        }
    };
    oReq.open('get', 'src/php/visitor_counter.php', true);
    oReq.send();
}
