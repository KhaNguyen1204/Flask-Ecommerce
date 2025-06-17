document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const clearButton = document.getElementById('clear-search');
    const filterButton = document.getElementById('filter-button');
    const resetButton = document.getElementById('reset-button');
    const searchStats = document.getElementById('search-stats');
    const visibleCount = document.getElementById('visible-count');
    const totalCount = document.getElementById('total-count');
    const totalDisplay = document.getElementById('total-display');
    const noResultsRow = document.getElementById('no-results-row');

    let searchTimeout;
    let originalContent = new Map(); // Store original content for each searchable element

    // Initialize
    initializeSearch();

    function initializeSearch() {
        // Store original content for highlighting
        document.querySelectorAll('.searchable-receipt-number, .searchable-supplier, .searchable-creator').forEach(element => {
            originalContent.set(element, element.textContent.trim());
        });

        // Event listeners
        searchInput.addEventListener('input', handleSearchInput);
        clearButton.addEventListener('click', clearSearch);
        document.getElementById('status-filter').addEventListener('change', debounceFilter);
        document.getElementById('warehouse-filter').addEventListener('change', debounceFilter);
        document.getElementById('start-date').addEventListener('change', debounceFilter);
        document.getElementById('end-date').addEventListener('change', debounceFilter);
        filterButton.addEventListener('click', filterReceipts);
        resetButton.addEventListener('click', resetFilters);

        // Enter key support
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                filterReceipts();
            }
        });
    }

    function handleSearchInput(e) {
        const value = e.target.value.trim();

        // Show/hide clear button
        clearButton.style.display = value ? 'block' : 'none';

        // Add loading effect
        searchInput.classList.add('loading-search');

        // Clear existing timeout
        clearTimeout(searchTimeout);

        // Debounce search
        searchTimeout = setTimeout(() => {
            searchInput.classList.remove('loading-search');
            filterReceipts();
        }, 300);
    }

    function clearSearch() {
        searchInput.value = '';
        clearButton.style.display = 'none';
        searchInput.focus();
        clearTimeout(searchTimeout);
        filterReceipts();
    }

    function debounceFilter() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(filterReceipts, 150);
    }

    function resetFilters() {
        // Clear all filters
        document.getElementById('status-filter').value = '';
        document.getElementById('warehouse-filter').value = '';
        searchInput.value = '';
        document.getElementById('start-date').value = '';
        document.getElementById('end-date').value = '';

        // Hide clear button
        clearButton.style.display = 'none';

        // Reset and filter
        clearTimeout(searchTimeout);
        filterReceipts();

        // Focus search input
        searchInput.focus();
    }

    function filterReceipts() {
        const status = document.getElementById('status-filter').value;
        const warehouse = document.getElementById('warehouse-filter').value;
        const searchTerm = searchInput.value.toLowerCase().trim();
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;

        const rows = document.querySelectorAll('.receipt-row');
        let visibleRows = 0;

        // Clear all highlights first
        clearHighlights();

        rows.forEach(row => {
            const rowStatus = row.getAttribute('data-status');
            const rowWarehouse = row.getAttribute('data-warehouse');
            const rowDate = row.getAttribute('data-date');
            const receiptNumber = row.getAttribute('data-receipt-number').toLowerCase();
            const supplier = row.getAttribute('data-supplier').toLowerCase();
            const creator = row.getAttribute('data-creator').toLowerCase();

            let visible = true;
            let searchMatch = false;

            // Filter by status
            if (status && rowStatus !== status) {
                visible = false;
            }

            // Filter by warehouse
            if (warehouse && rowWarehouse !== warehouse) {
                visible = false;
            }

            // Filter by date range
            if (startDate && rowDate < startDate) {
                visible = false;
            }
            if (endDate && rowDate > endDate) {
                visible = false;
            }

            // Search filter with highlighting
            if (searchTerm) {
                searchMatch = receiptNumber.includes(searchTerm) ||
                             supplier.includes(searchTerm) ||
                             creator.includes(searchTerm);

                if (!searchMatch) {
                    visible = false;
                } else {
                    // Highlight matching text
                    highlightText(row.querySelector('.searchable-receipt-number'), searchTerm);
                    highlightText(row.querySelector('.searchable-supplier'), searchTerm);
                    highlightText(row.querySelector('.searchable-creator'), searchTerm);
                }
            }

            // Show/hide row with animation
            if (visible) {
                row.style.display = '';
                row.classList.remove('fade-out');
                visibleRows++;
            } else {
                row.classList.add('fade-out');
                setTimeout(() => {
                    if (row.classList.contains('fade-out')) {
                        row.style.display = 'none';
                    }
                }, 300);
            }
        });

        // Update counters and show/hide elements
        updateSearchStats(visibleRows, rows.length, searchTerm || hasActiveFilters());

        // Show/hide no results message
        if (visibleRows === 0 && rows.length > 0) {
            noResultsRow.style.display = '';
        } else {
            noResultsRow.style.display = 'none';
        }
    }

    function clearHighlights() {
        document.querySelectorAll('.searchable-receipt-number, .searchable-supplier, .searchable-creator').forEach(element => {
            const original = originalContent.get(element);
            if (original) {
                element.innerHTML = original;
            }
        });
    }

    function highlightText(element, searchTerm) {
        if (!element || !searchTerm) return;

        const original = originalContent.get(element);
        if (!original) return;

        const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
        const highlighted = original.replace(regex, '<span class="highlight">$1</span>');
        element.innerHTML = highlighted;
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function hasActiveFilters() {
        return document.getElementById('status-filter').value ||
               document.getElementById('warehouse-filter').value ||
               document.getElementById('start-date').value ||
               document.getElementById('end-date').value;
    }

    function updateSearchStats(visible, total, showStats) {
        visibleCount.textContent = visible;
        totalCount.textContent = total;

        if (showStats) {
            searchStats.style.display = 'block';
            totalDisplay.style.display = 'none';
        } else {
            searchStats.style.display = 'none';
            totalDisplay.style.display = 'block';
            totalDisplay.textContent = `Tổng cộng: ${visible} phiếu`;
        }
    }

    // Initial filter
    filterReceipts();
});