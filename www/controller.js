$(document).ready(function () {

    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }

    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(receiverText)
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Hide Loader and display password input
    eel.expose(hideLoader)
    function hideLoader() {
        $("#Loader").attr("hidden", true);
        $("#PasswordAuth").attr("hidden", false);
    }

    // Handle password submission
    $("#PasswordSubmit").click(function() {
        var password = $("#PasswordInput").val();
        eel.verify_password(password)(function(result) {
            if (result) {
                $("#PasswordAuth").attr("hidden", true);
                $("#HelloGreet").attr("hidden", false);
            } else {
                $("#PasswordInput").val("");
                $("#PasswordInput").attr("placeholder", "Wrong password, try again");
            }
        });
    });

    // Handle Enter key press in password input
    $("#PasswordInput").keypress(function(e) {
        if (e.which == 13) {
            $("#PasswordSubmit").click();
        }
    });

    // Hide Start Page and display blob
    eel.expose(hideStart)
    function hideStart() {
        $("#Start").attr("hidden", true);
        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn");
        }, 1000)
        setTimeout(function () {
            $("#Oval").attr("hidden", false);
        }, 1000)
    }

    eel.expose(returnToIndex)
    function returnToIndex() {
        // Hide all other containers
        document.getElementById('chatContainer').style.display = 'none';
        document.getElementById('PasswordAuth').style.display = 'none';
        document.getElementById('HelloGreet').style.display = 'none';
        
        // Show the start page
        document.getElementById('startPage').style.display = 'flex';
        
        // Reset any active states
        document.getElementById('micButton').classList.remove('active');
        document.getElementById('micButton').style.animation = 'none';
        document.getElementById('micButton').offsetHeight; // Trigger reflow
        document.getElementById('micButton').style.animation = null;
    }
});