document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    const searchInput = document.getElementById('search-input');
    const statusFilter = document.getElementById('status-filter');
    const sortFilter = document.getElementById('sort-filter');
    const resetBtn = document.getElementById('reset-filter');
    const searchBtn = document.getElementById('search-btn');
    const searchClear = document.querySelector('.search-clear');
    const tbody = document.getElementById('warehouses-tbody');
    const warehouseCount = document.getElementById('warehouse-count');
    const noResultsRow = document.getElementById('no-results-row');

    let searchTimeout;

    function filterWarehouses() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const status = statusFilter.value;
        const sort = sortFilter.value;

        let rows = Array.from(document.querySelectorAll('.warehouse-row'));
        let visibleRows = [];

        // Filter
        rows.forEach(row => {
            let show = true;
            if (status && row.dataset.status !== status) show = false;

            if (searchTerm) {
                const name = row.dataset.name || '';
                const location = row.dataset.location || '';
                if (!name.includes(searchTerm) && !location.includes(searchTerm)) show = false;
            }

            row.style.display = show ? '' : 'none';
            if (show) visibleRows.push(row);
        });

        // Sort
        if (sort) {
            visibleRows.sort((a, b) => {
                if (sort === 'newest' || sort === 'oldest') {
                    const dateA = a.querySelector('td:nth-child(7)').textContent.trim().split('/').reverse().join('');
                    const dateB = b.querySelector('td:nth-child(7)').textContent.trim().split('/').reverse().join('');
                    return sort === 'newest' ? dateB.localeCompare(dateA) : dateA.localeCompare(dateB);
                }
                if (sort === 'capacity_high' || sort === 'capacity_low') {
                    const capA = parseInt(a.querySelector('td:nth-child(4)').textContent.trim()) || 0;
                    const capB = parseInt(b.querySelector('td:nth-child(4)').textContent.trim()) || 0;
                    return sort === 'capacity_high' ? capB - capA : capA - capB;
                }
                return 0;
            });
            // Re-append sorted rows
            visibleRows.forEach(row => tbody.appendChild(row));
        }

        // Update STT
        visibleRows.forEach((row, idx) => {
            const badge = row.querySelector('.badge.bg-secondary');
            if (badge) badge.textContent = idx + 1;
        });

        // Highlight
        clearHighlights();
        if (searchTerm) {
            visibleRows.forEach(row => {
                row.querySelectorAll('.searchable-content').forEach(cell => {
                    highlightText(cell, searchTerm);
                });
            });
        }

        // Show/hide no results
        if (noResultsRow) {
            noResultsRow.style.display = visibleRows.length === 0 ? '' : 'none';
        }

        // Update count
        if (warehouseCount) {
            warehouseCount.textContent = visibleRows.length
                ? `Hiển thị: ${visibleRows.length}/{{ warehouses|length }} kho`
                : `Tổng cộng: {{ warehouses|length }} kho`;
        }
    }

    function clearHighlights() {
        document.querySelectorAll('.searchable-content').forEach(cell => {
            const span = cell.querySelector('span');
            if (span) {
                span.innerHTML = span.textContent;
            }
        });
    }

    function highlightText(element, searchTerm) {
        const span = element.querySelector('span');
        if (!span) return;
        const text = span.textContent;
        const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
        span.innerHTML = text.replace(regex, '<span class="highlight">$1</span>');
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Event listeners
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        if (this.value.trim()) {
            if (searchClear) searchClear.style.display = 'block';
        } else {
            if (searchClear) searchClear.style.display = 'none';
        }
        searchTimeout = setTimeout(filterWarehouses, 300);
    });

    if (searchClear) {
        searchClear.addEventListener('click', function() {
            searchInput.value = '';
            searchClear.style.display = 'none';
            filterWarehouses();
            searchInput.focus();
        });
    }

    statusFilter.addEventListener('change', filterWarehouses);
    sortFilter.addEventListener('change', filterWarehouses);

    if (searchBtn) searchBtn.addEventListener('click', filterWarehouses);

    resetBtn.addEventListener('click', function() {
        searchInput.value = '';
        statusFilter.value = '';
        sortFilter.value = '';
        if (searchClear) searchClear.style.display = 'none';
        filterWarehouses();
        searchInput.focus();
    });

    // Initial filter
    filterWarehouses();
});