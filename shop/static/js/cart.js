
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

// Hiệu ứng icon tiêu đề
const cartIcon = document.querySelector('.cart-title i');
cartIcon.addEventListener('mouseenter', () => {
    cartIcon.style.transform = 'rotate(15deg) scale(1.1)';
});

cartIcon.addEventListener('mouseleave', () => {
    cartIcon.style.transform = 'rotate(0) scale(1)';
});

// Hiệu ứng khi hover vào hàng sản phẩm
const tableRows = document.querySelectorAll('.cart-table tbody tr:not(.summary-row)');
tableRows.forEach(row => {
    row.addEventListener('mouseenter', () => {
        row.style.transform = 'translateX(5px)';
    });

    row.addEventListener('mouseleave', () => {
        row.style.transform = 'translateX(0)';
    });
});

document.querySelectorAll('.quantity-input').forEach(function(input) {
    input.addEventListener('input', function() {
        let min = parseInt(this.min, 10);
        let max = parseInt(this.max, 10);
        let val = parseInt(this.value, 10);

        if (val < min) this.value = min;
        if (val > max) this.value = max;
    });
});