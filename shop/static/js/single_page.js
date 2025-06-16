
// Thumbnail image click handler
const mainImage = document.getElementById('main-image');
const thumbnails = document.querySelectorAll('.thumbnail-container img');

thumbnails.forEach(thumbnail => {
    thumbnail.addEventListener('click', () => {
        mainImage.style.opacity = '0';
        setTimeout(() => {
            mainImage.src = thumbnail.src;
            mainImage.style.opacity = '1';
        }, 200);

        thumbnails.forEach(img => img.classList.remove('active'));
        thumbnail.classList.add('active');
    });
});

// Quantity selector
const quantityInput = document.querySelector('#quantity');
const incrementBtn = document.querySelector('.increment-btn');
const decrementBtn = document.querySelector('.decrement-btn');

incrementBtn.addEventListener('click', () => {
    let value = parseInt(quantityInput.value);
    if (value < parseInt(quantityInput.max)) {
        quantityInput.value = value + 1;
    }
});

decrementBtn.addEventListener('click', () => {
    let value = parseInt(quantityInput.value);
    if (value > parseInt(quantityInput.min)) {
        quantityInput.value = value - 1;
    }
});

// Toggle reply form
document.querySelectorAll('.reply-toggle-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const reviewId = this.getAttribute('data-review');
        const form = document.querySelector(`#review-${reviewId} .reply-form`);
        if (form.style.display === 'none' || form.style.display === '') {
            form.style.display = 'block';
        } else {
            form.style.display = 'none';
        }
    });
});
