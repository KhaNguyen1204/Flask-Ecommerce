//Js cho trang quản lý thương hiệu
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const clearSearch = document.getElementById('clearSearch');
    const itemRows = document.querySelectorAll('.item-row');
    const noResultsMessage = document.getElementById('noResultsMessage');
    const totalItemsSpan = document.getElementById('totalItems');
    const searchResultsSpan = document.getElementById('searchResults');
    
    // Xử lý tìm kiếm
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim().toLowerCase();
        let matchedItems = 0;
        
        // Hiển thị nút xóa khi có nội dung
        clearSearch.style.display = searchTerm ? 'block' : 'none';
        
        itemRows.forEach(row => {
            const itemName = row.getAttribute('data-item-name');
            const nameCell = row.querySelector('.item-name');
            const originalName = nameCell.dataset.original || nameCell.textContent;
            
            // Lưu tên gốc nếu chưa có
            if (!nameCell.dataset.original) {
                nameCell.dataset.original = originalName;
            }
            
            // Highlight và lọc
            if (searchTerm === '' || itemName.includes(searchTerm)) {
                row.style.display = '';
                matchedItems++;
                
                // Highlight từ khóa nếu có
                if (searchTerm) {
                    const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
                    nameCell.innerHTML = originalName.replace(regex, '<span class="bg-warning">$1</span>');
                } else {
                    nameCell.textContent = originalName;
                }
            } else {
                row.style.display = 'none';
                nameCell.textContent = originalName;
            }
        });
        
        // Hiển thị thông báo khi không có kết quả
        if (searchTerm && matchedItems === 0) {
            noResultsMessage.style.display = 'block';
            searchResultsSpan.style.display = 'none';
        } else {
            noResultsMessage.style.display = 'none';
            
            // Cập nhật số lượng kết quả
            if (searchTerm) {
                searchResultsSpan.textContent = `Tìm thấy: ${matchedItems}`;
                searchResultsSpan.style.display = 'inline';
                totalItemsSpan.style.display = 'none';
            } else {
                searchResultsSpan.style.display = 'none';
                totalItemsSpan.style.display = 'inline';
            }
        }
    });
    
    // Xóa tìm kiếm
    clearSearch.addEventListener('click', function() {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        searchInput.focus();
    });
    
    // Hàm escape ký tự đặc biệt cho regex
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
});