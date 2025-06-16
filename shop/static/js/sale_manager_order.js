
    document.addEventListener('DOMContentLoaded', function () {
        const searchInput = document.getElementById('searchInput');
        const clearSearchBtn = document.getElementById('clearSearch');
        const orderRows = document.querySelectorAll('.hover-row');

        function highlightText(element, searchTerm) {
            if (!element || !searchTerm) return;

            if (!element.dataset.original) {
                element.dataset.original = element.innerHTML;
            }

            const text = element.textContent;
            const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
            const highlightedText = text.replace(regex, '<span class="highlight">$1</span>');
            element.innerHTML = highlightedText;
        }

        function escapeRegExp(string) {
            return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }

        function removeHighlights() {
            document.querySelectorAll('[data-original]').forEach(el => {
                el.innerHTML = el.dataset.original;
                delete el.dataset.original;
            });
        }

        function performSearch() {
            const searchTerm = searchInput.value.trim();
            removeHighlights();

            if (!searchTerm) {
                orderRows.forEach(row => row.style.display = '');
                return;
            }

            const lowerSearchTerm = searchTerm.toLowerCase();
            let hasResults = false;

            orderRows.forEach(row => {
                const invoiceElement = row.querySelector('h6');
                const customerElement = row.querySelector('.col-2:nth-child(3) small');

                const invoice = invoiceElement?.textContent.toLowerCase() || '';
                const customer = customerElement?.textContent.toLowerCase() || '';

                if (invoice.includes(lowerSearchTerm) || customer.includes(lowerSearchTerm)) {
                    row.style.display = '';
                    hasResults = true;

                    // Highlight matching text
                    if (invoice.includes(lowerSearchTerm)) {
                        highlightText(invoiceElement, searchTerm);
                    }
                    if (customer.includes(lowerSearchTerm)) {
                        highlightText(customerElement, searchTerm);
                    }
                } else {
                    row.style.display = 'none';
                }
            });
        }

        // Event listeners
        searchInput.addEventListener('input', function () {
            performSearch();
            clearSearchBtn.style.display = this.value ? 'block' : 'none';
        });

        clearSearchBtn.addEventListener('click', function () {
            searchInput.value = '';
            performSearch();
            clearSearchBtn.style.display = 'none';
            searchInput.focus();
        });
    });
