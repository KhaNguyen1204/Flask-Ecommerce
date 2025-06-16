document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Lọc kho theo trạng thái
    document.getElementById('status-filter').addEventListener('change', filterWarehouses);

    // Sắp xếp kho
    document.getElementById('sort-filter').addEventListener('change', filterWarehouses);

    // Reset bộ lọc
    document.getElementById('reset-filter').addEventListener('click', function() {
        document.getElementById('status-filter').value = '';
        document.getElementById('sort-filter').value = '';
        document.getElementById('search-input').value = '';
        filterWarehouses();
    });

    // Tìm kiếm kho
    document.getElementById('search-input').addEventListener('keyup', filterWarehouses);

    function filterWarehouses() {
        const statusFilter = document.getElementById('status-filter').value;
        const searchTerm = document.getElementById('search-input').value.toLowerCase();

        document.querySelectorAll('.warehouse-row').forEach(function(row) {
            let showRow = true;

            if (statusFilter && row.dataset.status !== statusFilter) {
                showRow = false;
            }

            if (searchTerm) {
                const warehouseName = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
                const warehouseLocation = row.querySelector('td:nth-child(3)').textContent.toLowerCase();
                if (!warehouseName.includes(searchTerm) && !warehouseLocation.includes(searchTerm)) {
                    showRow = false;
                }
            }

            row.style.display = showRow ? '' : 'none';
        });
    }
});

