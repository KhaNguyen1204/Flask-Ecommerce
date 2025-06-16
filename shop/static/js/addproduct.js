
// Thêm hiệu ứng nổi
const floatingContainer = document.querySelector('.floating-elements');
for (let i = 0; i < 5; i++) {
    const element = document.createElement('div');
    element.classList.add('floating-element');
    const size = Math.random() * 80 + 20;
    element.style.width = `${size}px`;
    element.style.height = `${size}px`;
    element.style.top = `${Math.random() * 100}%`;
    element.style.left = `${Math.random() * 100}%`;
    element.style.animationDelay = `-${Math.random() * 15}s`;
    element.style.animationDuration = `${Math.random() * 10 + 10}s`;
    floatingContainer.appendChild(element);
}

// Hiệu ứng icon khi hover
const headerIcon = document.querySelector('.form-header i');
headerIcon.addEventListener('mouseenter', () => {
    headerIcon.style.transform = 'rotate(15deg) scale(1.1)';
});

headerIcon.addEventListener('mouseleave', () => {
    headerIcon.style.transform = 'rotate(0) scale(1)';
});

// Hiệu ứng khi focus vào input
const inputs = document.querySelectorAll('.form-control, .form-select');
inputs.forEach(input => {
    input.addEventListener('focus', () => {
        input.style.borderColor = '#17a2b8';
        input.previousElementSibling.style.color = '#17a2b8';
    });

    input.addEventListener('blur', () => {
        input.style.borderColor = '#e9ecef';
        if (!input.value) {
            input.previousElementSibling.style.color = '#495057';
        }
    });
});
