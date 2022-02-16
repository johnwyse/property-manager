function show_report_issue_form_inline() {
    console.log("issue button clicked")

    document.querySelector(".report-issue-form").style.display = "inline-block";     
}

function show_report_issue_form_block() {
    console.log("issue button clicked")

    document.querySelector(".report_an_issue_form").style.display = "block";     
}

function show_send_message_form_inline() {
    console.log("send message button clicked")

    document.querySelector("#send-message-form").style.display = "inline-block";
}

function show_send_message_form_block() {
    console.log("send message button clicked")

    document.querySelector(".send_a_message_form").style.display = "block";
}


function show_issue_textarea(id) {
    console.log("beginning to show issue textarea")
    console.log(id)

    document.querySelector(`#edit_issue_area_${id}`).style.display = "block";
    document.querySelector(`#original_issue_description_${id}`).style.display = "none";
}


function update_issue(id) {
    console.log("begin updating post")
    console.log(id)

    // Get new content of post
    const updated_description = document.querySelector(`#updated_description_${id}`).value;
    console.log(updated_description)

    // Fetch and save updated content
    fetch('/edit_issue/' + id, {
        method: 'PUT',
        body: JSON.stringify({
            description: updated_description
        })
    })
    .catch(error => { 
        console.log('Error:', error)
    });
    console.log("update saved, now showing updated version")

    document.querySelector(`#current_issue_description_${id}`).innerHTML = `Description: ${updated_description}`;
    document.querySelector(`#edit_issue_area_${id}`).style.display = "none";
    document.querySelector(`#original_issue_description_${id}`).style.display = "block";
}

function delete_message(message_id) {
    console.log("beginning to delete message")
    console.log(message_id)

    fetch('delete_message/' + message_id, {
        method: 'DELETE',
        body: JSON.stringify({
            message_id: message_id
        })
    })
    .catch(error => {
        console.log("Error: " + error);
    });

    console.log("now beginning to hide div")
    
    // Hide div and animate slide up

    const div_to_hide = document.querySelector(`#delete_button_${message_id}`)
    console.log(div_to_hide.parentElement.parentElement)
    div_to_hide.parentElement.parentElement.style.animationPlayState = 'running';


}