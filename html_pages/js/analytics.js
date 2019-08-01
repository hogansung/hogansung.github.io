/* Google Analyitcs API */
window.ga=window.ga||function(){(ga.q=ga.q||[]).push(arguments)};ga.l=+new Date;
ga('create', 'UA-112083134-2', 'auto');
ga('send', 'pageview');


/* Google Analytics Retrieve Data */
function initClient() {
    gapi.client.init({
        'apiKey': "AIzaSyBmnQ62un-WZqpYaLbW32EBW7E6J7vFX-s",
        // clientId and scope are optional if auth is not required.
        'client_id': "247748488144-8fnt0j1dts299u7stmh3hbk8l0jcln7f.apps.googleusercontent.com",
        'scope': 'https://www.googleapis.com/auth/analytics.readonly',
    }).then(function() {
        gapi.client.request({
            path: '/v4/reports:batchGet',
            root: 'https://analyticsreporting.googleapis.com/',
            method: 'POST',
            body: {
                reportRequests: [
                    {
                        viewId: '193833568',
                        dateRanges: [
                            {
                                startDate: '7daysAgo',
                                endDate: 'today'
                            }
                        ],
                        metrics: [
                            {
                                expression: 'ga:users'
                            }
                        ]
                    }
                ]
            }
        }).then(function(response) {
            total_number_visit = response.result["reports"][0]["data"]["totals"][0]["values"][0];
            for (i = 0; i < 6; i++) {
                document.getElementById('d' + i).innerHTML = total_number_visit % 10;
                total_number_visit = Math.floor(total_number_visit / 10);
            }
        }, console.error.bind(console));
    });
};
