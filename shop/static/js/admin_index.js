document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearch');
    const productRows = document.querySelectorAll('.product-row');
    const totalProducts = document.getElementById('totalProducts');
    const searchResults = document.getElementById('searchResults');
    const noResultsMessage = document.getElementById('noResultsMessage');
    const productsTable = document.getElementById('productsTable');
    const totalCount = productRows.length; // Sửa lại cách lấy tổng số sản phẩm

    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;

        // Clear previous highlights
        document.querySelectorAll('.highlight').forEach(el => {
            const parent = el.parentNode;
            parent.replaceChild(document.createTextNode(el.textContent), el);
        });

        productRows.forEach(row => {
            const productName = row.getAttribute('data-product-name').toLowerCase();
            const brandName = row.getAttribute('data-brand-name').toLowerCase();
            const displayStyle = (searchTerm === '' ||
                productName.includes(searchTerm) ||
                brandName.includes(searchTerm)) ? '' : 'none';

            row.style.display = displayStyle;

            if (displayStyle === '') {
                visibleCount++;

                // Highlight matching text
                if (searchTerm !== '') {
                    highlightText(row.querySelector('.product-name'), searchTerm);
                    highlightText(row.querySelector('.brand-name'), searchTerm);
                }
            }
        });

        // Update UI based on search results
        if (searchTerm === '') {
            totalProducts.style.display = '';
            searchResults.style.display = 'none';
            noResultsMessage.style.display = 'none';
            productsTable.style.display = '';
        } else {
            totalProducts.style.display = 'none';
            searchResults.style.display = '';
            searchResults.textContent = `Tìm thấy: ${visibleCount} sản phẩm`;

            noResultsMessage.style.display = visibleCount === 0 ? 'block' : 'none';
            productsTable.style.display = visibleCount === 0 ? 'none' : '';
        }
    }

    function highlightText(element, searchTerm) {
        if (!element || searchTerm === '') return;

        const text = element.textContent;
        const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
        element.innerHTML = text.replace(regex, '<span class="highlight bg-warning">$1</span>');
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Event listeners with debounce
    let searchTimeout;
    searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(performSearch, 300);
    });

    searchInput.addEventListener('keyup', function (e) {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            performSearch();
        }
    });

    clearSearchBtn.addEventListener('click', function () {
        searchInput.value = '';
        performSearch();
        searchInput.focus();
    });

    // Toggle clear button visibility
    searchInput.addEventListener('input', function () {
        clearSearchBtn.style.display = this.value ? 'block' : 'none';
    });

    // Initialize
    clearSearchBtn.style.display = 'none';
});