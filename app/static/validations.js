document.addEventListener('DOMContentLoaded', function() {
    var currentForm = document.querySelector('form');
    if (currentForm!=null){
        var currentFormId = currentForm.id;
    }

    // Check the current form and call the respective validation function
    if(currentFormId=='loginForm'){
        loginValidation(currentFormId);
    }else if (currentFormId=='registerForm'){
        registerValidation(currentFormId);
    }
})


function loginValidation(currentFormId){
    // Handle form submission event for login form
    document.getElementById(currentFormId).addEventListener('submit', function (event) {
        errorBox.textContent = '';
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        
        // Validate username length
        if (username.length>24) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Username must be 24 characters or less\n';
            errorBox.style.display = 'block';
        }

        var alphanumericPattern = /^[a-zA-Z0-9]+$/;
        // Validate username alphanumeric pattern
        if (!alphanumericPattern.test(username)) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Username should contain only alphanumeric characters.\n';
            errorBox.style.display = 'block';
        }

    });

    document.getElementById('submit').addEventListener('click', function () {
        document.getElementById(currentFormId).submit();
    });
}


function registerValidation(currentFormId){
    // Handle form submission event for register form
    document.getElementById(currentFormId).addEventListener('submit', function (event) {

        errorBox.textContent = '';

        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        var email = document.getElementById('email').value;

        // Validate username length
        if (username.length>24) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Username must be 24 characters or less. \n';
            errorBox.style.display = 'block';
        }

        // Validate password length
        if (password.length<6) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Password must be 6 characters or more \n';
            errorBox.style.display = 'block';
        }

        var alphanumericPattern = /^[a-zA-Z0-9]+$/;
        // Validate username alphanumeric pattern
        if (!alphanumericPattern.test(username)) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Username should contain only alphanumeric characters.\n';
            errorBox.style.display = 'block';
        }


        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        // Validate email format
        if (!emailPattern.test(email)) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Invalid Email format. Please check email. \n';
            errorBox.style.display = 'block';
        }

    });
    // Handle form submission event when submit button is clicked
    document.getElementById('submit').addEventListener('click', function () {
        document.getElementById(currentFormId).submit();
    });
}


