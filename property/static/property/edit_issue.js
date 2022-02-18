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

    document.querySelector(`#current_issue_description_${id}`).innerHTML = `Description:<br>${updated_description}`;
    document.querySelector(`#edit_issue_area_${id}`).style.display = "none";
    document.querySelector(`#original_issue_description_${id}`).style.display = "block";
}