
document.addEventListener('DOMContentLoaded', function () {
    // Enhanced table row hover effects
    const tableRows = document.querySelectorAll('.modern-table tbody tr');

    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function () {
            this.style.transform = 'translateX(5px)';
        });

        row.addEventListener('mouseleave', function () {
            this.style.transform = 'translateX(0)';
        });
    });

    // Print functionality enhancement
    const printBtn = document.querySelector('.print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function () {
            // Add print-specific styles
            document.body.classList.add('printing');

            setTimeout(() => {
                window.print();
                document.body.classList.remove('printing');
            }, 100);
        });
    }

    // Smooth scroll to sections
    const cardHeaders = document.querySelectorAll('.card-header');
    cardHeaders.forEach(header => {
        header.addEventListener('click', function () {
            this.parentElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });
});

// Print event handling
window.addEventListener('beforeprint', function () {
    document.body.style.background = 'white';
});

window.addEventListener('afterprint', function () {
    document.body.style.background = '';
});
