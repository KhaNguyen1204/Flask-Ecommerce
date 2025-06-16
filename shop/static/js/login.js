  document.addEventListener('DOMContentLoaded', function() {
    // Hiệu ứng cho các field khi được focus
    const formInputs = document.querySelectorAll('.form-control');

    formInputs.forEach(input => {
      input.addEventListener('focus', function() {
        this.style.transform = 'translateY(-3px)';
        this.style.boxShadow = '0 5px 15px rgba(0, 123, 255, 0.1)';
      });

      input.addEventListener('blur', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = 'none';
      });
    });

    // Hiệu ứng cho button login
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn) {
      loginBtn.addEventListener('mouseover', function() {
        this.style.animation = 'pulse 0.8s ease-in-out infinite';
      });

      loginBtn.addEventListener('mouseout', function() {
        this.style.animation = 'none';
      });
    }

    // Thêm icon nếu chưa có FontAwesome
    if (!document.querySelector('link[href*="font-awesome"]')) {
      const iconPlaceholders = document.querySelectorAll('.input-icon i');
      iconPlaceholders.forEach(icon => {
        icon.style.display = 'none';
      });

      const inputs = document.querySelectorAll('.input-icon input');
      inputs.forEach(input => {
        input.style.paddingLeft = '15px';
      });
    }
  });