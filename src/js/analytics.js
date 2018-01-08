/* Google Analyitcs API */
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'UA-112083134-1');


/* Google Analytics Retrieve Data */
function initClient() {
    gapi.client.init({
        'apiKey': "AIzaSyBkTPfX55NRxmd9pZVNhs2yT-1fE75litE",
        // clientId and scope are optional if auth is not required.
        'client_id': "247748488144-snvkg0rq81f293cuo70itn4iu9lhlnf8.apps.googleusercontent.com",
        'scope': 'profile',
    }).then(function() {
        gapi.client.request({
            path: '/v4/reports:batchGet',
            root: 'https://analyticsreporting.googleapis.com/',
            method: 'POST',
            body: {
                reportRequests: [
                    {
                        viewId: '167398842',
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
