
// Gallery thumbnail click
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
