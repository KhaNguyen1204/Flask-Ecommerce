
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const item = question.parentElement;
        const answer = question.nextElementSibling;
        const isActive = question.classList.contains('active');

        // Close all other items
        document.querySelectorAll('.faq-question.active').forEach(activeQuestion => {
            if (activeQuestion !== question) {
                activeQuestion.classList.remove('active');
                activeQuestion.nextElementSibling.classList.remove('active');
            }
        });

        // Toggle current item
        if (isActive) {
            question.classList.remove('active');
            answer.classList.remove('active');
        } else {
            question.classList.add('active');
            answer.classList.add('active');
        }
    });
});

// Search functionality
const searchInput = document.getElementById('searchInput');
const faqItems = document.querySelectorAll('.faq-item');
const faqSections = document.querySelectorAll('.faq-section');
const noResults = document.querySelector('.no-results');

searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    let hasResults = false;

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question span').textContent.toLowerCase();
        const answer = item.querySelector('.faq-answer').textContent.toLowerCase();
        
        if (question.includes(searchTerm) || answer.includes(searchTerm)) {
            item.style.display = 'block';
            hasResults = true;
            
            // Highlight search terms
            const questionElement = item.querySelector('.faq-question span');
            const originalText = questionElement.textContent;
            if (searchTerm && question.includes(searchTerm)) {
                const regex = new RegExp(`(${searchTerm})`, 'gi');
                questionElement.innerHTML = originalText.replace(regex, '<span class="highlight">$1</span>');
            } else {
                questionElement.textContent = originalText;
            }
        } else {
            item.style.display = 'none';
        }
    });

    // Show/hide sections based on results
    faqSections.forEach(section => {
        const visibleItems = section.querySelectorAll('.faq-item[style="display: block;"], .faq-item:not([style*="display: none"])');
        section.style.display = visibleItems.length > 0 ? 'block' : 'none';
    });

    // Show/hide no results message
    if (hasResults || searchTerm === '') {
        noResults.classList.remove('show');
    } else {
        noResults.classList.add('show');
    }
});

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', () => {
    // Add some smooth animations on load
    const items = document.querySelectorAll('.faq-item');
    items.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
    });
});