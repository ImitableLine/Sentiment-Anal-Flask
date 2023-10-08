$(document).ready(function () {
    // Add a click event listener to the "Get Predictions" button
    $("#getDataButton").click(function () {
        // Get the user input from the input field
        var user_input = $("#twitterLinkInput").val();
    
        // Make an AJAX POST request to the Flask server
        $.ajax({
            type: "POST",
            url: "/predict",
            data: {
                twitter_link: user_input
            },
            success: function (response) {
                try {
                    // Verify that response.predictions exists and is an array
                    if (response && response.predictions && Array.isArray(response.predictions)) {
                        // Process the predictions here
                        var predictions = response.predictions;
                        var resultHtml = "<h3>Predictions for Twitter comments:</h3>";
    
                        for (var i = 0; i < predictions.length; i++) {
                            resultHtml += '<div class="comment-box">';
                            resultHtml += '<p>' + predictions[i].comment + '</p>';
                            resultHtml += '<p>Sentiment: ' + predictions[i].sentiment + '</p>';
                            resultHtml += '<p>Confidence: ' + predictions[i].confidence.toFixed(4) + '</p>'; // Format confidence
                            resultHtml += '</div>';
                        }
    
                        $('#twitterData').html(resultHtml); // Display predictions in the "twitterData" div
                    } else {
                        console.error('Invalid response data:', response);
                    }
                } catch (error) {
                    console.error('Error handling response:', error);
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });
    // Handle the "Predict on URL" button click
    $('#predictOnURLButton').click(function () {
        // Get the video URL entered by the user
        var videoUrl = $('#videoUrlInput').val();

        // Make an AJAX request to your Flask server to trigger YouTube comment collection and prediction
        $.ajax({
            url: '/predict_youtube',
            type: 'POST',
            data: { video_url: videoUrl },
            success: function (response) {
                try {
                    // Verify that response.predictions exists and is an array
                    if (response && response.predictions && Array.isArray(response.predictions)) {
                        // Process the predictions here
                        var predictions = response.predictions;
                        var resultHtml = "<h3>Predictions for YouTube comments:</h3>";

                        for (var i = 0; i < predictions.length; i++) {
                            resultHtml += '<div class="comment-box">';
                            resultHtml += '<p>' + predictions[i].comment + '</p>';
                            resultHtml += '<p>Sentiment: ' + predictions[i].sentiment + '</p>';
                            resultHtml += '<p>Confidence: ' + predictions[i].confidence.toFixed(4) + '</p>'; // Format confidence
                            resultHtml += '</div>';
                        }

                        $('#youtubeData').html(resultHtml); // Display predictions in the "youtubeData" div
                    } else {
                        console.error('Invalid response data:', response);
                    }
                } catch (error) {
                    console.error('Error handling response:', error);
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });
});