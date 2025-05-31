document.addEventListener('DOMContentLoaded', function () {
    // Валидация формы регистрации
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            event.preventDefault();
            let isValid = true;

            const errorMessages = registerForm.querySelectorAll('.error-message');
            errorMessages.forEach(error => {
                error.textContent = '';
                error.classList.remove('active');
            });

            const emailField = registerForm.querySelector('#id_email');
            const usernameField = registerForm.querySelector('#id_username');
            const password1Field = registerForm.querySelector('#id_password1');
            const password2Field = registerForm.querySelector('#id_password2');

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const domainRegex = /^[^\s@]+@([^\s@]+)\.([a-zA-Z]{2,})$/;
            if (!emailField.value) {
                showError(emailField, 'email-error', 'Email обязателен');
                isValid = false;
            } else if (!emailRegex.test(emailField.value)) {
                showError(emailField, 'email-error', 'Введите корректный email');
                isValid = false;
            } else if (!domainRegex.test(emailField.value)) {
                showError(emailField, 'email-error', 'Доменная часть email некорректна (например, example.com)');
                isValid = false;
            }

            const usernameRegex = /^[a-zA-Z0-9_]+$/;
            if (!usernameField.value) {
                showError(usernameField, 'username-error', 'Имя пользователя обязательно');
                isValid = false;
            } else if (!usernameRegex.test(usernameField.value)) {
                showError(usernameField, 'username-error', 'Имя пользователя может содержать только буквы, цифры и подчеркивания');
                isValid = false;
            } else if (usernameField.value.length < 3) {
                showError(usernameField, 'username-error', 'Имя пользователя должно быть не короче 3 символов');
                isValid = false;
            }

            if (!password1Field.value) {
                showError(password1Field, 'password1-error', 'Пароль обязателен');
                isValid = false;
            } else if (password1Field.value.length < 8) {
                showError(password1Field, 'password1-error', 'Пароль должен содержать не менее 8 символов');
                isValid = false;
            }

            if (password1Field.value !== password2Field.value) {
                showError(password2Field, 'password2-error', 'Пароли не совпадают');
                isValid = false;
            }

            if (isValid) {
                registerForm.submit();
            }
        });
    }

    // Валидация формы входа
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            let isValid = true;

            const errorMessages = loginForm.querySelectorAll('.error-message');
            errorMessages.forEach(error => {
                error.textContent = '';
                error.classList.remove('active');
            });

            const usernameField = loginForm.querySelector('#id_username');
            const passwordField = loginForm.querySelector('#id_password');

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const domainRegex = /^[^\s@]+@([^\s@]+)\.([a-zA-Z]{2,})$/;
            const usernameRegex = /^[a-zA-Z0-9_]+$/;
            if (!usernameField.value) {
                showError(usernameField, 'username-error', 'Имя пользователя или email обязательны');
                isValid = false;
            } else if (!emailRegex.test(usernameField.value) && !usernameRegex.test(usernameField.value)) {
                showError(usernameField, 'username-error', 'Введите корректное имя пользователя или email');
                isValid = false;
            } else if (emailRegex.test(usernameField.value) && !domainRegex.test(usernameField.value)) {
                showError(usernameField, 'username-error', 'Доменная часть email некорректна (например, example.com)');
                isValid = false;
            }

            if (!passwordField.value) {
                showError(passwordField, 'password-error', 'Пароль обязателен');
                isValid = false;
            } else if (passwordField.value.length < 8) {
                showError(passwordField, 'password-error', 'Пароль должен содержать не менее 8 символов');
                isValid = false;
            }

            if (isValid) {
                loginForm.submit();
            }
        });
    }

    // Валидация формы обратной связи
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();
            let isValid = true;

            const errorMessages = contactForm.querySelectorAll('.error-message');
            errorMessages.forEach(error => {
                error.textContent = '';
                error.classList.remove('active');
            });

            const nameField = contactForm.querySelector('#id_name');
            const emailField = contactForm.querySelector('#id_email');
            const messageField = contactForm.querySelector('#id_message');

            if (!nameField.value) {
                showError(nameField, 'name-error', 'Имя обязательно');
                isValid = false;
            } else if (nameField.value.length < 2) {
                showError(nameField, 'name-error', 'Имя должно содержать не менее 2 символов');
                isValid = false;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const domainRegex = /^[^\s@]+@([^\s@]+)\.([a-zA-Z]{2,})$/;
            if (!emailField.value) {
                showError(emailField, 'email-error', 'Email обязателен');
                isValid = false;
            } else if (!emailRegex.test(emailField.value)) {
                showError(emailField, 'email-error', 'Введите корректный email');
                isValid = false;
            } else if (!domainRegex.test(emailField.value)) {
                showError(emailField, 'email-error', 'Доменная часть email некорректна (например, example.com)');
                isValid = false;
            }

            if (!messageField.value) {
                showError(messageField, 'message-error', 'Сообщение обязательно');
                isValid = false;
            } else if (messageField.value.length < 10) {
                showError(messageField, 'message-error', 'Сообщение должно содержать не менее 10 символов');
                isValid = false;
            }

            if (isValid) {
                contactForm.submit();
            }
        });
    }

    // Функция для отображения ошибок
    function showError(field, errorId, message) {
        const errorElement = document.getElementById(`id_${errorId}`);
        errorElement.textContent = message;
        errorElement.classList.add('active');
        field.classList.add('error');
    }
});