document.addEventListener('DOMContentLoaded', function() {
    let searchTimeout;
    let currentSearchTerm = '';
    const originalRowCount = {{ receipts|length }};

    // DOM elements
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const warehouseFilter = document.getElementById('warehouse-filter');
    const dateFromFilter = document.getElementById('date-from');
    const dateToFilter = document.getElementById('date-to');
    const resetButton = document.getElementById('reset-filter');
    const clearSearchButton = document.getElementById('clear-search');
    const searchButton = document.getElementById('filter-button'); // Sửa ID
    const searchSpinner = document.querySelector('.search-spinner');
    const searchClear = document.querySelector('.search-clear');
    const searchResultsInfo = document.getElementById('search-results-info');
    const resultsText = document.getElementById('results-text');
    const totalCount = document.getElementById('total-count');

    // Kiểm tra DOM elements
    console.log('DOM elements:', {
        searchInput, statusFilter, warehouseFilter, dateFromFilter, dateToFilter,
        resetButton, clearSearchButton, searchButton, searchSpinner, searchClear,
        searchResultsInfo, resultsText, totalCount
    });

    // Initialize
    if (resetButton) {
        initializeSearch();
    } else {
        console.error('Reset button not found');
    }

    function initializeSearch() {
        // Debounced search on input
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const value = this.value.trim();
            if (value !== currentSearchTerm) {
                showSearchSpinner();
                searchTimeout = setTimeout(performSearch, 300);
            }
        });

        // Real-time filter changes
        [statusFilter, warehouseFilter, dateFromFilter, dateToFilter].forEach(element => {
            if (element) {
                element.addEventListener('change', performSearch);
            }
        });

        // Search button click
        if (searchButton) {
            searchButton.addEventListener('click', performSearch);
        }

        // Clear search
        if (searchClear) {
            searchClear.addEventListener('click', clearSearch);
        }
        if (clearSearchButton) {
            clearSearchButton.addEventListener('click', clearSearch);
        }

        // Reset all filters
        resetButton.addEventListener('click', function() {
            console.log('Reset button clicked');
            resetAllFilters();
        });

        // Enter key on search input
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }

    function showSearchSpinner() {
        if (searchSpinner) searchSpinner.style.display = 'block';
        if (searchClear) searchClear.style.display = 'none';
        searchInput.classList.add('searching');
    }

    function hideSearchSpinner() {
        if (searchSpinner) searchSpinner.style.display = 'none';
        searchInput.classList.remove('searching');
        if (searchInput.value.trim() && searchClear) {
            searchClear.style.display = 'block';
        }
    }

    function performSearch() {
        showSearchSpinner();
        setTimeout(() => {
            const searchTerm = searchInput.value.trim().toLowerCase();
            const status = statusFilter.value;
            const warehouse = warehouseFilter.value;
            const dateFrom = dateFromFilter.value;
            const dateTo = dateToFilter.value;
            currentSearchTerm = searchTerm;

            clearHighlights();
            const rows = document.querySelectorAll('.receipt-row');
            let visibleCount = 0;
            let hasActiveFilters = searchTerm || status || warehouse || dateFrom || dateTo;

            console.log('Performing search with:', { searchTerm, status, warehouse, dateFrom, dateTo });

            rows.forEach((row, index) => {
                const isVisible = checkRowVisibility(row, searchTerm, status, warehouse, dateFrom, dateTo);
                if (isVisible) {
                    visibleCount++;
                    showRow(row, index);
                    if (searchTerm) highlightSearchTerm(row, searchTerm);
                } else {
                    hideRow(row);
                }
            });

            updateSearchResults(visibleCount, hasActiveFilters, searchTerm);
            updateRowNumbers();
            hideSearchSpinner();
        }, 100);
    }

    function checkRowVisibility(row, searchTerm, status, warehouse, dateFrom, dateTo) {
        if (status && row.getAttribute('data-status') !== status) return false;
        if (warehouse && row.getAttribute('data-warehouse') !== warehouse) return false;

        if (dateFrom || dateTo) {
            const dateText = row.getAttribute('data-receipt-date');
            const parts = dateText.split('/');
            const rowDate = new Date(parts[2], parts[1] - 1, parts[0]);

            if (dateFrom && rowDate < new Date(dateFrom)) return false;
            if (dateTo && rowDate > new Date(dateTo)) return false;
        }

        if (searchTerm) {
            const receiptNumber = row.getAttribute('data-receipt-number').toLowerCase();
            const warehouseName = row.getAttribute('data-warehouse-name').toLowerCase();
            const creatorName = row.getAttribute('data-creator-name').toLowerCase();
            const searchableText = `${receiptNumber} ${warehouseName} ${creatorName}`;
            const searchTerms = searchTerm.split(' ').filter(term => term.length > 0);
            return searchTerms.every(term => searchableText.includes(term));
        }

        return true;
    }

    function showRow(row, index) {
        console.log(`Showing row ${index}:`, row);
        row.style.display = 'table-row';
        row.classList.remove('fade-out');
        row.classList.add('fade-in');
        setTimeout(() => {
            row.classList.remove('fade-in');
        }, 500);
    }

    function hideRow(row) {
        row.classList.add('fade-out');
        setTimeout(() => {
            row.style.display = 'none';
            row.classList.remove('fade-out');
        }, 300);
    }

    function highlightSearchTerm(row, searchTerm) {
        const searchableElements = row.querySelectorAll('.searchable-content');
        const searchTerms = searchTerm.split(' ').filter(term => term.length > 0);

        searchableElements.forEach(element => {
            const textNode = element.querySelector('span') || element;
            let originalText = textNode.getAttribute('data-original-text') || textNode.textContent;

            if (!textNode.getAttribute('data-original-text')) {
                textNode.setAttribute('data-original-text', originalText);
            }

            let highlightedText = originalText;
            searchTerms.forEach(term => {
                const regex = new RegExp(`(${escapeRegExp(term)})`, 'gi');
                highlightedText = highlightedText.replace(regex, '<span class="highlight">$1</span>');
            });

            textNode.innerHTML = highlightedText;
        });
    }

    function clearHighlights() {
        const highlightedElements = document.querySelectorAll('.searchable-content span[data-original-text]');
        highlightedElements.forEach(element => {
            const originalText = element.getAttribute('data-original-text');
            if (originalText) {
                element.textContent = originalText;
                element.removeAttribute('data-original-text');
            }
        });
    }

    function updateSearchResults(visibleCount, hasActiveFilters, searchTerm) {
        if (hasActiveFilters) {
            searchResultsInfo.style.display = 'block';
            let message = `Hiển thị ${visibleCount} trong tổng số ${originalRowCount} phiếu`;
            if (searchTerm) message += ` cho từ khóa "${searchTerm}"`;
            resultsText.textContent = message;
            totalCount.textContent = `Hiển thị: ${visibleCount}/${originalRowCount} phiếu`;
        } else {
            searchResultsInfo.style.display = 'none';
            totalCount.textContent = `Tổng cộng: ${originalRowCount} phiếu`;
        }
    }

    function updateRowNumbers() {
        const visibleRows = document.querySelectorAll('.receipt-row[style="display: table-row;"], .receipt-row:not([style])');
        visibleRows.forEach((row, index) => {
            const numberCell = row.querySelector('.badge.bg-secondary');
            if (numberCell) numberCell.textContent = index + 1;
        });
    }

    function clearSearch() {
        searchInput.value = '';
        if (searchClear) searchClear.style.display = 'none';
        currentSearchTerm = '';
        performSearch();
        searchInput.focus();
    }

    function resetAllFilters() {
        console.log('Resetting all filters...');
        searchInput.value = '';
        statusFilter.value = '';
        warehouseFilter.value = '';
        dateFromFilter.value = '';
        dateToFilter.value = '';

        if (searchClear) searchClear.style.display = 'none';
        if (searchResultsInfo) searchResultsInfo.style.display = 'none';

        clearHighlights();
        currentSearchTerm = '';

        const rows = document.querySelectorAll('.receipt-row');
        console.log('Total rows to reset:', rows.length);
        rows.forEach((row, index) => {
            setTimeout(() => {
                showRow(row, index);
            }, index * 50);
        });

        updateRowNumbers();
        totalCount.textContent = `Tổng cộng: ${originalRowCount} phiếu`;
        searchInput.focus();
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Initialize clear button visibility
    searchInput.addEventListener('input', function() {
        if (this.value.trim() && searchClear) {
            searchClear.style.display = 'block';
        } else if (searchClear) {
            searchClear.style.display = 'none';
        }
    });
});