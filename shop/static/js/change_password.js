
    document.addEventListener('DOMContentLoaded', function() {
    // Validate password match
    const passwordForm = document.getElementById('passwordForm');
    const newPasswordInput = document.querySelector('[name="new_password"]');
    const confirmInput = document.querySelector('[name="confirm"]');

    passwordForm.addEventListener('submit', function(event) {
        if (newPasswordInput.value !== confirmInput.value) {
        event.preventDefault();
        alert('Mật khẩu mới và xác nhận mật khẩu không khớp!');
        }
    });

    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const target = document.getElementById(targetId);

        if (target.type === 'password') {
            target.type = 'text';
            this.classList.remove('fa-eye-slash');
            this.classList.add('fa-eye');
        } else {
            target.type = 'password';
            this.classList.remove('fa-eye');
            this.classList.add('fa-eye-slash');
        }
        });
    });

    // Check password strength
    function checkPasswordStrength(password) {
        // Initialize variables
        let strength = 0;
        let tips = [];

        // If password is 8 chars or more, increase strength
        if (password.length >= 8) {
        strength += 25;
        } else {
        tips.push("Mật khẩu nên có ít nhất 8 ký tự");
        }

        // If password contains lowercase and uppercase characters, increase strength
        if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
        strength += 25;
        } else {
        tips.push("Nên có cả chữ hoa và chữ thường");
        }

        // If password contains numbers, increase strength
        if (password.match(/([0-9])/)) {
        strength += 25;
        } else {
        tips.push("Nên có ít nhất 1 số");
        }

        // If password contains special chars, increase strength
        if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) {
        strength += 25;
        } else {
        tips.push("Nên có ít nhất 1 ký tự đặc biệt");
        }

        return {
        strength: strength,
        tips: tips
        };
    }

    // Update password strength meter
    newPasswordInput.addEventListener('input', function() {
        const strengthResult = checkPasswordStrength(this.value);
        const strengthBar = document.querySelector('.password-strength');
        const strengthText = document.querySelector('.strength-text');

        // Update the strength bar
        strengthBar.style.width = strengthResult.strength + '%';

        // Update color and text based on strength
        if (strengthResult.strength < 25) {
        strengthBar.style.backgroundColor = '#dc3545'; // red
        strengthText.innerText = 'Rất yếu';
        strengthText.style.color = '#dc3545';
        } else if (strengthResult.strength < 50) {
        strengthBar.style.backgroundColor = '#ffc107'; // yellow
        strengthText.innerText = 'Yếu';
        strengthText.style.color = '#ffc107';
        } else if (strengthResult.strength < 75) {
        strengthBar.style.backgroundColor = '#0dcaf0'; // cyan
        strengthText.innerText = 'Trung bình';
        strengthText.style.color = '#0dcaf0';
        } else if (strengthResult.strength < 100) {
        strengthBar.style.backgroundColor = '#198754'; // green
        strengthText.innerText = 'Mạnh';
        strengthText.style.color = '#198754';
        } else {
        strengthBar.style.backgroundColor = '#198754'; // green
        strengthText.innerText = 'Rất mạnh';
        strengthText.style.color = '#198754';
        }

        // Show tips if there are any
        if (strengthResult.tips.length > 0 && this.value) {
        strengthText.innerText += ': ' + strengthResult.tips.join(', ');
        }
    });

    // Enable bootstrap components
    const alerts = document.querySelectorAll('.alert')
    alerts.forEach(function (alert) {
        new bootstrap.Alert(alert)
    })
    });
