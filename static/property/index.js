document.addEventListener('DOMContentLoaded', function() {

    document.getElementById("show_report_issue_form").addEventListener('click', () => {

        console.log("issue button clicked")
        if (document.getElementById("report_issue_toggle").style.display === "none") {
            console.log("opening")
            document.getElementById("report_issue_toggle").style.display = "inline-block";
        } else {
            console.log("closing")
            document.getElementById("report_issue_toggle").style.display = "none";
        }
    })

    
    
    document.getElementById("show_send_message_form").addEventListener('click', () => {

    console.log("message button clicked")
    if (document.getElementById("send_message_toggle").style.display === "none") {
        console.log("opening")
        document.getElementById("send_message_toggle").style.display = "inline-block";
    } else {
        console.log("closing")
        document.getElementById("send_message_toggle").style.display = "none";
    }
    })

})
