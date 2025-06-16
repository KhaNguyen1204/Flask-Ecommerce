document.addEventListener('DOMContentLoaded', function () {
const searchInput = document.getElementById('searchInput');
const clearSearch = document.getElementById('clearSearch');
const staffRows = document.querySelectorAll('.staff-row');

function highlightText(element, searchTerm) {
    if (!element) return;
    const text = element.textContent;
    if (!searchTerm) {
        element.innerHTML = text;
        return;
    }
    const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
    element.innerHTML = text.replace(regex, '<span class="highlight">$1</span>');
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function filterAndHighlight() {
    const searchTerm = searchInput.value.trim();
    clearSearch.style.display = searchTerm ? 'block' : 'none';
    const searchTermLower = searchTerm.toLowerCase();
    staffRows.forEach(row => {
        const nameEl = row.querySelector('.staff-name');
        const emailEl = row.querySelector('.staff-email');
        const phoneEl = row.querySelector('.staff-phone');
        const name = nameEl.textContent.toLowerCase();
        const email = emailEl.textContent.toLowerCase();
        const phone = phoneEl.textContent.toLowerCase();
        const matches = name.includes(searchTermLower) || email.includes(searchTermLower) || phone.includes(searchTermLower);
        if (matches) {
            row.style.display = '';
            highlightText(nameEl, searchTerm);
            highlightText(emailEl, searchTerm);
            highlightText(phoneEl, searchTerm);
        } else {
            row.style.display = 'none';
            highlightText(nameEl, '');
            highlightText(emailEl, '');
            highlightText(phoneEl, '');
        }
    });
}

searchInput.addEventListener('input', filterAndHighlight);
clearSearch.addEventListener('click', function () {
    searchInput.value = '';
    filterAndHighlight();
    searchInput.focus();
});
filterAndHighlight();
});
