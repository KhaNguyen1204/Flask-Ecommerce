document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearch');
    const productRows = document.querySelectorAll('.product-row');
    const totalProducts = document.getElementById('totalProducts');
    const searchResults = document.getElementById('searchResults');
    const noResults = document.getElementById('noResults');
    const productTableBody = document.getElementById('productTableBody');
    const totalCount = {{ products|length }};

    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;

        // Clear previous highlights
        document.querySelectorAll('.highlight').forEach(el => {
            el.outerHTML = el.innerHTML;
        });

        productRows.forEach(row => {
            const productName = row.getAttribute('data-name');
            const brandName = row.getAttribute('data-brand');
            const nameCell = row.querySelector('.product-name');
            const brandCell = row.querySelector('.product-brand');

            if (searchTerm === '' ||
                productName.includes(searchTerm) ||
                brandName.includes(searchTerm)) {

                row.style.display = '';
                visibleCount++;

                // Highlight matching text
                if (searchTerm !== '') {
                    highlightText(nameCell, searchTerm);
                    highlightText(brandCell, searchTerm);
                } else {
                    nameCell.innerHTML = nameCell.textContent;
                    brandCell.innerHTML = brandCell.textContent;
                }
            } else {
                row.style.display = 'none';
            }
        });

        // Update result counter
        if (searchTerm === '') {
            totalProducts.style.display = '';
            searchResults.style.display = 'none';
            noResults.style.display = 'none';
            productTableBody.style.display = '';
        } else {
            totalProducts.style.display = 'none';
            searchResults.style.display = '';
            searchResults.textContent = `Tìm thấy: ${visibleCount} sản phẩm`;

            if (visibleCount === 0) {
                noResults.style.display = 'block';
                productTableBody.style.display = 'none';
            } else {
                noResults.style.display = 'none';
                productTableBody.style.display = '';
            }
        }
    }

    function highlightText(element, searchTerm) {
        if (!element) return;
        const text = element.textContent;
        const regex = new RegExp(`(${searchTerm})`, 'gi');
        const highlightedText = text.replace(regex, '<span class="highlight">$1</span>');
        element.innerHTML = highlightedText;
    }

    // Event listeners
    searchInput.addEventListener('input', performSearch);
    searchInput.addEventListener('keyup', function (e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    clearSearchBtn.addEventListener('click', function () {
        searchInput.value = '';
        performSearch();
        searchInput.focus();
    });

    // Show/hide clear button based on input
    searchInput.addEventListener('input', function () {
        clearSearchBtn.style.display = this.value ? 'block' : 'none';
    });

    // Initialize clear button visibility
    clearSearchBtn.style.display = 'none';

    // Confirm delete with double-click prevention
    document.querySelectorAll('form[action*="deleteproduct"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Đang xóa...';
        });
});