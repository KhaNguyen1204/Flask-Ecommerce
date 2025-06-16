
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

// Hiệu ứng khi hover vào card
const productCards = document.querySelectorAll('.product-card');
productCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        const img = card.querySelector('.product-img');
        img.style.transform = 'scale(1.1)';
    });
    
    card.addEventListener('mouseleave', () => {
        const img = card.querySelector('.product-img');
        img.style.transform = 'scale(1)';
    });
});