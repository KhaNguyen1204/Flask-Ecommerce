// home_index.js
// Thêm hiệu ứng nổi động
const floatingContainer = document.querySelector('.floating-elements');

// Tạo thêm các phần tử nổi ngẫu nhiên
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

// Tối ưu hiệu ứng hover cho card
const productCards = document.querySelectorAll('.product-card');
productCards.forEach(card => {
    let hoverTimeout;

    card.addEventListener('mouseenter', () => {
        clearTimeout(hoverTimeout);
        const img = card.querySelector('.product-img');
        if (img && img.classList.contains('loaded')) {
            img.style.transform = 'scale(1.1)';
        }
    });

    card.addEventListener('mouseleave', () => {
        const img = card.querySelector('.product-img');
        if (img) {
            hoverTimeout = setTimeout(() => {
                img.style.transform = 'scale(1)';
            }, 50);
        }
    });
});

// Xử lý lazy loading và error cho ảnh
const images = document.querySelectorAll('.product-img');

// Intersection Observer cho lazy loading hiệu quả hơn
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            if (img.src && !img.classList.contains('loaded') && !img.classList.contains('error')) {
                // Đã có src, chỉ cần đợi load
                if (img.complete) {
                    img.classList.add('loaded');
                }
            }
            observer.unobserve(img);
        }
    });
}, {
    rootMargin: '50px'
});

images.forEach(img => {
    imageObserver.observe(img);

    // Xử lý khi ảnh load thành công
    img.addEventListener('load', function() {
        this.classList.add('loaded');
    });

    // Xử lý khi ảnh lỗi
    img.addEventListener('error', function() {
        this.classList.add('error');
        this.alt = 'Không có ảnh';
    });
});

// Tối ưu hiệu suất scroll
let ticking = false;

function updateScrollEffects() {
    // Có thể thêm các hiệu ứng scroll tại đây
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(updateScrollEffects);
        ticking = true;
    }
});

// Preload ảnh quan trọng
function preloadCriticalImages() {
    const firstRowImages = document.querySelectorAll('.product-card:nth-child(-n+4) .product-img');
    firstRowImages.forEach(img => {
        if (img.src && !img.classList.contains('loaded')) {
            const preloadImg = new Image();
            preloadImg.onload = () => img.classList.add('loaded');
            preloadImg.onerror = () => img.classList.add('error');
            preloadImg.src = img.src;
        }
    });
}

// Chạy preload sau khi DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', preloadCriticalImages);
} else {
    preloadCriticalImages();
}

// Format giá tiền cho các phần tử được load động
function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN').format(price);
}

// Accessibility improvements
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        const focusedElement = document.activeElement;
        if (focusedElement.classList.contains('product-card')) {
            const detailsLink = focusedElement.querySelector('.btn-details');
            if (detailsLink) {
                detailsLink.click();
            }
        }
    }
});
