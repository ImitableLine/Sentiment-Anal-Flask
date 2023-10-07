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
                // Update the "Response is displayed here" div with the prediction result
                $("#twitterData").html("User Input: " + response.user_input + "<br>Sentiment: " + response.sentiment + "<br>Confidence: " + response.confidence);
            }
        });
    });
});