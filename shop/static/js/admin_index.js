
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
        const noResultsMessage = document.getElementById('noResultsMessage');
        const productsTable = document.getElementById('productsTable');
        const totalCount = {{ products|length }};

        function performSearch() {
            const searchTerm = searchInput.value.toLowerCase().trim();
            let visibleCount = 0;

            // Clear previous highlights
            document.querySelectorAll('.highlight').forEach(el => {
                el.outerHTML = el.innerHTML;
            });

            productRows.forEach(row => {
                const productName = row.getAttribute('data-product-name');
                const brandName = row.getAttribute('data-brand-name');

                if (searchTerm === '' ||
                    productName.includes(searchTerm) ||
                    brandName.includes(searchTerm)) {

                    row.style.display = '';
                    visibleCount++;

                    // Highlight matching text
                    if (searchTerm !== '') {
                        highlightText(row.querySelector('.product-name'), searchTerm);
                        highlightText(row.querySelector('.brand-name'), searchTerm);
                    }
                } else {
                    row.style.display = 'none';
                }
            });

            // Update result counter
            if (searchTerm === '') {
                totalProducts.style.display = '';
                searchResults.style.display = 'none';
                noResultsMessage.style.display = 'none';
                productsTable.style.display = '';
            } else {
                totalProducts.style.display = 'none';
                searchResults.style.display = '';
                searchResults.textContent = `Tìm thấy: ${visibleCount} sản phẩm`;

                if (visibleCount === 0) {
                    noResultsMessage.style.display = 'block';
                    productsTable.style.display = 'none';
                } else {
                    noResultsMessage.style.display = 'none';
                    productsTable.style.display = '';
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
    });
