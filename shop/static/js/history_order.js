
// Highlight row on click
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.table-hover tbody tr').forEach(function(row) {
        row.addEventListener('click', function() {
            document.querySelectorAll('.table-hover tbody tr').forEach(r => r.classList.remove('table-active'));
            this.classList.add('table-active');
        });
    });
    // Enable Bootstrap tooltips
    if (window.bootstrap) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});
