document.addEventListener('DOMContentLoaded', function() {
    let searchTimeout;
    let currentSearchTerm = '';
    const originalRowCount = window.originalRowCount || 0;

    // DOM elements
    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const warehouseFilter = document.getElementById('warehouse-filter');
    const dateFromFilter = document.getElementById('date-from');
    const dateToFilter = document.getElementById('date-to');
    const resetButton = document.getElementById('reset-filter');
    const clearSearchButton = document.getElementById('clear-search');
    const searchButton = document.getElementById('search-btn');
    const searchSpinner = document.querySelector('.search-spinner');
    const searchClear = document.querySelector('.search-clear');
    const searchResultsInfo = document.getElementById('search-results-info');
    const resultsText = document.getElementById('results-text');
    const totalCount = document.getElementById('total-count');
    const noResultsRow = document.getElementById('no-results-row');

    // Initialize
    initializeSearch();

    function initializeSearch() {
        // Debounced search on input
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const value = this.value.trim();

            if (value !== currentSearchTerm) {
                showSearchSpinner();
                searchTimeout = setTimeout(() => {
                    performSearch();
                }, 300); // 300ms debounce
            }
        });

        // Real-time filter changes
        [statusFilter, warehouseFilter, dateFromFilter, dateToFilter].forEach(element => {
            element.addEventListener('change', performSearch);
        });

        // Search button click
        if (searchButton) searchButton.addEventListener('click', performSearch);

        // Clear search
        if (searchClear) searchClear.addEventListener('click', clearSearch);
        if (clearSearchButton) clearSearchButton.addEventListener('click', clearSearch);

        // Reset all filters
        if (resetButton) resetButton.addEventListener('click', resetAllFilters);

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

            // Clear previous highlights
            clearHighlights();

            const rows = document.querySelectorAll('.receipt-row');
            let visibleCount = 0;
            let hasActiveFilters = searchTerm || status || warehouse || dateFrom || dateTo;

            rows.forEach((row, index) => {
                const isVisible = checkRowVisibility(row, searchTerm, status, warehouse, dateFrom, dateTo);

                if (isVisible) {
                    visibleCount++;
                    showRow(row, index);

                    // Highlight search term
                    if (searchTerm) {
                        highlightSearchTerm(row, searchTerm);
                    }
                } else {
                    hideRow(row);
                }
            });

            // Update UI
            updateSearchResults(visibleCount, hasActiveFilters, searchTerm);
            updateRowNumbers();
            hideSearchSpinner();

            // Show/hide no results row
            if (noResultsRow) {
                if (visibleCount === 0 && rows.length > 0) {
                    noResultsRow.style.display = '';
                } else {
                    noResultsRow.style.display = 'none';
                }
            }
        }, 100); // Small delay for smooth UX
    }

    function checkRowVisibility(row, searchTerm, status, warehouse, dateFrom, dateTo) {
        // Status filter
        if (status && row.getAttribute('data-status') !== status) {
            return false;
        }

        // Warehouse filter
        if (warehouse && row.getAttribute('data-warehouse') !== warehouse) {
            return false;
        }

        // Date filters
        if (dateFrom || dateTo) {
            const dateText = row.getAttribute('data-receipt-date');
            const parts = dateText.split('/');
            const rowDate = new Date(parts[2], parts[1] - 1, parts[0]);

            if (dateFrom) {
                const from = new Date(dateFrom);
                if (rowDate < from) return false;
            }

            if (dateTo) {
                const to = new Date(dateTo);
                if (rowDate > to) return false;
            }
        }

        // Search term filter
        if (searchTerm) {
            const receiptNumber = row.getAttribute('data-receipt-number').toLowerCase();
            const warehouseName = row.getAttribute('data-warehouse-name').toLowerCase();
            const creatorName = row.getAttribute('data-creator-name').toLowerCase();

            const searchableText = `${receiptNumber} ${warehouseName} ${creatorName}`;

            // Support multiple search terms
            const searchTerms = searchTerm.split(' ').filter(term => term.length > 0);
            return searchTerms.every(term => searchableText.includes(term));
        }

        return true;
    }

    function showRow(row, index) {
        row.style.display = '';
        row.classList.remove('fade-out');
        row.classList.add('fade-in');

        // Remove animation class after animation completes
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

            // Store original text if not already stored
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
            if (searchResultsInfo) searchResultsInfo.style.display = 'block';

            let message = `Hiển thị ${visibleCount} trong tổng số ${originalRowCount} phiếu`;
            if (searchTerm) {
                message += ` cho từ khóa "${searchTerm}"`;
            }
            if (resultsText) resultsText.textContent = message;

            if (totalCount) totalCount.textContent = `Hiển thị: ${visibleCount}/${originalRowCount} phiếu`;
        } else {
            if (searchResultsInfo) searchResultsInfo.style.display = 'none';
            if (totalCount) totalCount.textContent = `Tổng cộng: ${originalRowCount} phiếu`;
        }
    }

    function updateRowNumbers() {
        const visibleRows = document.querySelectorAll('.receipt-row[style=""], .receipt-row:not([style])');
        visibleRows.forEach((row, index) => {
            const numberCell = row.querySelector('.badge.bg-secondary');
            if (numberCell) {
                numberCell.textContent = index + 1;
            }
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
        // Clear all inputs
        searchInput.value = '';
        statusFilter.value = '';
        warehouseFilter.value = '';
        dateFromFilter.value = '';
        dateToFilter.value = '';

        // Hide search elements
        if (searchClear) searchClear.style.display = 'none';
        if (searchResultsInfo) searchResultsInfo.style.display = 'none';

        // Clear highlights and reset
        clearHighlights();
        currentSearchTerm = '';

        // Show all rows with animation
        const rows = document.querySelectorAll('.receipt-row');
        rows.forEach((row, index) => {
            setTimeout(() => {
                showRow(row, index);
            }, index * 50); // Staggered animation
        });

        // Update UI
        updateRowNumbers();
        if (totalCount) totalCount.textContent = `Tổng cộng: ${originalRowCount} phiếu`;

        // Focus search input
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

    // Initial filter
    performSearch();
});