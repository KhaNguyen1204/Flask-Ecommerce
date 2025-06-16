document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const resetFilterBtn = document.getElementById('reset-filter');
    const categoryFilter = document.getElementById('category-filter');
    const brandFilter = document.getElementById('brand-filter');
    const productsTableBody = document.getElementById('products-table-body');
    const productCountEl = document.getElementById('product-count');

    const noResultsRow = document.createElement('tr');
    noResultsRow.className = 'no-results';
    noResultsRow.innerHTML = `
        <td colspan="10" class="text-center py-5">
            <i class="fas fa-search text-muted" style="font-size: 3rem;"></i>
            <h5 class="text-muted mt-3">Không có kết quả phù hợp</h5>
            <p class="text-muted">Hãy thử từ khóa tìm kiếm khác hoặc điều chỉnh bộ lọc</p>
        </td>
    `;

    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearSearchBtn.classList.toggle('d-none', this.value === '');
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            filterProducts();
        }, 300);
    });

    clearSearchBtn.addEventListener('click', function() {
        searchInput.value = '';
        clearSearchBtn.classList.add('d-none');
        filterProducts();
    });

    categoryFilter.addEventListener('change', filterProducts);
    brandFilter.addEventListener('change', filterProducts);

    resetFilterBtn.addEventListener('click', function() {
        searchInput.value = '';
        categoryFilter.value = '';
        brandFilter.value = '';
        clearSearchBtn.classList.add('d-none');
        filterProducts();
    });

    function filterProducts() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const categoryValue = categoryFilter.value;
        const brandValue = brandFilter.value;

        let visibleCount = 0;
        let hasResults = false;

        clearHighlights();

        document.querySelectorAll('.product-row').forEach((row, index) => {
            const productName = row.querySelector('.product-name').textContent.toLowerCase();
            const categoryName = row.dataset.categoryName || '';
            const brandName = row.dataset.brandName || '';

            const categoryMatch = !categoryValue || row.dataset.category === categoryValue;
            const brandMatch = !brandValue || row.dataset.brand === brandValue;
            const searchMatch = !searchTerm ||
                               productName.includes(searchTerm) ||
                               categoryName.includes(searchTerm) ||
                               brandName.includes(searchTerm);

            const shouldShow = categoryMatch && brandMatch && searchMatch;

            if (shouldShow) {
                row.style.display = '';
                visibleCount++;
                hasResults = true;

                const sttBadge = row.querySelector('.badge.bg-secondary');
                if (sttBadge) {
                    sttBadge.textContent = visibleCount;
                }

                if (searchTerm) {
                    highlightSearchResults(row, searchTerm);
                }
            } else {
                row.style.display = 'none';
            }
        });

        productCountEl.textContent = visibleCount;
        handleNoResults(hasResults);
    }

    function clearHighlights() {
        document.querySelectorAll('.highlight').forEach(el => {
            const parent = el.parentNode;
            parent.replaceChild(document.createTextNode(el.textContent), el);
            parent.normalize();
        });
    }

    function highlightSearchResults(row, searchTerm) {
        const elementsToHighlight = [
            row.querySelector('.product-name'),
            row.querySelector('.product-category'),
            row.querySelector('.product-brand')
        ];

        elementsToHighlight.forEach(element => {
            if (element && element.textContent.toLowerCase().includes(searchTerm)) {
                highlightText(element, searchTerm);
            }
        });
    }

    function highlightText(element, searchTerm) {
        const text = element.textContent;
        const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
        const newHTML = text.replace(regex, '<span class="highlight">$1</span>');
        element.innerHTML = newHTML;
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function handleNoResults(hasResults) {
        const noResultsElement = document.querySelector('.no-results');
        const noProductsElement = document.querySelector('.no-products');

        if (!hasResults && !noProductsElement) {
            if (!noResultsElement) {
                productsTableBody.appendChild(noResultsRow);
            }
        } else {
            if (noResultsElement) {
                noResultsElement.remove();
            }
        }
    }

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(tooltipTriggerEl => {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
