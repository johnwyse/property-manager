document.addEventListener('DOMContentLoaded', function() {

    fetch('/get_notifications')
    .then(response => response.json())
    .then(data => {
        
        // Change innerHTML of the navbar
        if (data.unread != 0) {
            document.getElementById('messages_nav').innerHTML = `Messages(${data.unread})`
        }
        if (data.unresolved != 0) {
            document.getElementById('issues_nav').innerHTML = `Issues(${data.unresolved})`
        }
        
    })
    .catch(error => { 
        console.log('Error:', error)
    });
    
    return false

})


function show_report_issue_form_block() {
    console.log("issue button clicked")

    document.querySelector(".report_an_issue_form").style.display = "block";     
}

function show_send_message_form_block() {
    console.log("send message button clicked")

    document.querySelector(".send_a_message_form").style.display = "block";
}

