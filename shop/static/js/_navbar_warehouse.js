document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.warehouse-navbar .nav-link:not(.dropdown-toggle)');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            link.closest('.nav-item').classList.add('active');
        }
    });
    const dropdownItems = document.querySelectorAll('.warehouse-navbar .dropdown-item');
    dropdownItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
            const dropdownToggle = item.closest('.dropdown-menu').previousElementSibling;
            if (dropdownToggle && dropdownToggle.classList.contains('dropdown-toggle')) {
                dropdownToggle.classList.add('active');
            }
        }
    });
});
