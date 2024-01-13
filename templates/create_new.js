function saveData() {
    var dataName = document.getElementById('dataName').value;
    var email = document.getElementById('email').value;
    
    // Add CSRF token to the headers
    var csrfToken = document.head.querySelector("[name=csrf-token]").content;

    // Make an AJAX request to the Flask route
    jQuery.ajax({
        type: 'POST',
        url: '/create_new',
        data: {
            'dataName': dataName,
            'email': email,
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {
            alert(response.message);
        },
        error: function (error) {
            console.error('Error saving data:', error);
        }
    });
}