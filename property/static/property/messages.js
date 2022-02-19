document.addEventListener('DOMContentLoaded', function() {

    var unit_id = JSON.parse(document.getElementById('unit_id').textContent);
    console.log(unit_id)

    fetch('/property/mark_as_read/' + unit_id, {
        method: 'PUT',
        body: JSON.stringify({
          unit_id: unit_id
        })
      })
      .catch(error => { 
        console.log('Error:', error)
      });
    
    

    document.getElementById("dropdown_button").addEventListener('click', () => {

      console.log("dropdown button clicked")
      if (document.getElementById("dropdown_toggle").style.display === "none") {
          console.log("opening")
          document.getElementById("dropdown_toggle").style.display = "block";
      } else {
          console.log("closing")
          document.getElementById("dropdown_toggle").style.display = "none";
      }
      })

    return false
})

function delete_message(message_id) {
    console.log("beginning to delete message")
    console.log(message_id)

    fetch('/property/delete_message/' + message_id, {
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
    const button = document.querySelector(`#delete_button_${message_id}`);
    let div_to_hide = button.parentElement.parentElement;
    div_to_hide.style.animationPlayState = 'running';

}