document.addEventListener('DOMContentLoaded', function() {
    var currentForm = document.querySelector('form');
    if (currentForm!=null){
        var currentFormId = currentForm.id;
    }

    if(currentFormId=='loginForm'){
        loginValidation(currentFormId);
    }else if (currentFormId=='registerForm'){
        registerValidation(currentFormId);
    }
})


function loginValidation(currentFormId){
    document.getElementById(currentFormId).addEventListener('submit', function (event) {
        errorBox.textContent = '';
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        
        if (username.length>24) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Username must be 24 characters or less\n';
            errorBox.style.display = 'block';
        }

        var alphanumericPattern = /^[a-zA-Z0-9]+$/;
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
    document.getElementById(currentFormId).addEventListener('submit', function (event) {

        errorBox.textContent = '';

        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        var email = document.getElementById('email').value;

        
        if (username.length>24) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Username must be 24 characters or less. \n';
            errorBox.style.display = 'block';
        }

        var alphanumericPattern = /^[a-zA-Z0-9]+$/;
        if (!alphanumericPattern.test(username)) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Username should contain only alphanumeric characters.\n';
            errorBox.style.display = 'block';
        }


        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            event.preventDefault(); // Prevent form submission
            errorBox.textContent += 'Invalid Email format. Please check email. \n';
            errorBox.style.display = 'block';
        }

    });

    document.getElementById('submit').addEventListener('click', function () {
        document.getElementById(currentFormId).submit();
    });
}


