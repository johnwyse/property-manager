document.addEventListener('DOMContentLoaded', function() {

    var unit_id = JSON.parse(document.getElementById('unit_id').textContent);
    console.log(unit_id)

    fetch('/mark_as_read/' + unit_id, {
        method: 'PUT',
        body: JSON.stringify({
          unit_id: unit_id
        })
      })
      .catch(error => { 
        console.log('Error:', error)
      });
    
      return false

})