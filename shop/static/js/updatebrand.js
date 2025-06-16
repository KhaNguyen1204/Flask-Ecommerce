
document.addEventListener('DOMContentLoaded', function() {
    // Enhanced form input interactions
    const formInput = document.querySelector('.form-input');
    
    if (formInput) {
        // Auto-focus on load
        setTimeout(() => formInput.focus(), 500);
        
        // Enhanced focus effects
        formInput.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        formInput.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Enter key submission
        formInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.querySelector('.btn-primary').click();
            }
        });
    }
    
    // Form submission with loading state
    const form = document.querySelector('form');
    const submitBtn = document.querySelector('.btn-primary');
    
    if (form && submitBtn) {
        form.addEventListener('submit', function() {
            submitBtn.style.opacity = '0.7';
            submitBtn.style.transform = 'scale(0.98)';
            submitBtn.innerHTML = '<i class="bi bi-arrow-repeat icon" style="animation: spin 1s linear infinite;"></i><span>Đang xử lý...</span>';
        });
    }
    
    // Add spin animation for loading state
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
});
