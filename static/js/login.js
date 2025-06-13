// Login Page JavaScript Functionality

// Password toggle functionality
function togglePassword() {
    const passwordInput = document.querySelector('input[type="password"]');
    const toggleIcon = document.getElementById('toggleIcon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.login-form');
    const inputs = document.querySelectorAll('.modern-input');
    const loginBtn = document.querySelector('.btn-login');

    // Enhanced input focus effects
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });

    // Form validation
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;

            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                return;
            }

            // Show loading state
            if (loginBtn) {
                loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Se conectează...';
                loginBtn.disabled = true;
            }
        });
    }

    // Remember me functionality
    const rememberCheckbox = document.getElementById('remember-me');
    const usernameInput = document.querySelector('input[name="username"]');

    if (rememberCheckbox && usernameInput) {
        // Load saved credentials
        if (localStorage.getItem('rememberMe') === 'true') {
            rememberCheckbox.checked = true;
            const savedUsername = localStorage.getItem('savedUsername');
            if (savedUsername) {
                usernameInput.value = savedUsername;
            }
        }

        // Save credentials on form submit
        if (form) {
            form.addEventListener('submit', function() {
                if (rememberCheckbox.checked) {
                    localStorage.setItem('rememberMe', 'true');
                    localStorage.setItem('savedUsername', usernameInput.value);
                } else {
                    localStorage.removeItem('rememberMe');
                    localStorage.removeItem('savedUsername');
                }
            });
        }
    }

    // Auto-focus first empty input
    const firstEmptyInput = Array.from(inputs).find(input => !input.value.trim());
    if (firstEmptyInput) {
        firstEmptyInput.focus();
    }
});
