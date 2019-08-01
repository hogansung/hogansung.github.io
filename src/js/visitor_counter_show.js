$(window).load(function(){
    $('#visitor_counter').load("/visitor_counter.html", function(){
        var oReq = new XMLHttpRequest();
        oReq.onload = function() {
            var total_number_visit = JSON.parse(this.responseText);
            for (i = 0; i < 6; i++) {
                document.getElementById('d' + i).innerHTML = total_number_visit % 10;
                total_number_visit = Math.floor(total_number_visit / 10);
            }
        };
        oReq.open('get', '/php/visitor_counter_show.php', true);
        oReq.send();
    });
});
