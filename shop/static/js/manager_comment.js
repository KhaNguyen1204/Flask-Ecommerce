
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const productTableBody = document.getElementById('productTableBody');
    const noResultsDiv = document.getElementById('noResults');
    const originalRows = Array.from(productTableBody.querySelectorAll('tr'));

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim().toLowerCase();
        let hasResults = false;

        // Reset all rows and highlights
        originalRows.forEach(row => {
            row.style.display = 'none';
            const productNameCell = row.querySelector('.product-name');
            productNameCell.innerHTML = productNameCell.textContent;
        });

        if (searchTerm === '') {
            originalRows.forEach(row => row.style.display = '');
            noResultsDiv.style.display = 'none';
            return;
        }

        originalRows.forEach(row => {
            const productName = row.getAttribute('data-product-name');
            if (productName.includes(searchTerm)) {
                hasResults = true;
                row.style.display = '';

                // Highlight matching text
                const productNameCell = row.querySelector('.product-name');
                const text = productNameCell.textContent;
                const regex = new RegExp(searchTerm, 'gi');
                const highlightedText = text.replace(regex, match =>
                    `<span class="highlight">${match}</span>`
                );
                productNameCell.innerHTML = highlightedText;
            }
        });

        noResultsDiv.style.display = hasResults ? 'none' : 'block';
    });
});
