document.addEventListener('DOMContentLoaded', function() {

    fetch('/property/get_notifications')
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