
document.addEventListener('DOMContentLoaded', function() {
    // Thêm dòng chi tiết mới
    document.getElementById('add-detail').addEventListener('click', function() {
        var detailsContainer = document.getElementById('receipt-details');
        var newRow = detailsContainer.querySelector('.receipt-detail-row').cloneNode(true);

        // Reset giá trị
        newRow.querySelectorAll('input').forEach(function(input) {
            if (input.type !== 'hidden') {
                input.value = input.type === 'number' ? (input.min || 0) : '';
            }
        });
        newRow.querySelector('select').selectedIndex = 0;

        detailsContainer.appendChild(newRow);
        attachEventListeners();
        calculateTotals();
    });

    // Xóa dòng chi tiết
    function attachRemoveListener(removeBtn) {
        removeBtn.addEventListener('click', function() {
            var detailsContainer = document.getElementById('receipt-details');
            if (detailsContainer.querySelectorAll('.receipt-detail-row').length > 1) {
                this.closest('.receipt-detail-row').remove();
                calculateTotals();
            } else {
                alert('Phiếu xuất phải có ít nhất một sản phẩm!');
            }
        });
    }

    // Tính toán thành tiền và tổng tiền
    function calculateSubtotal(row) {
        var quantity = parseFloat(row.querySelector('.quantity-input').value) || 0;
        var price = parseFloat(row.querySelector('.price-input').value) || 0;
        var subtotal = quantity * price;

        row.querySelector('.subtotal-input').value = subtotal;
        row.querySelector('.subtotal-display').value = formatCurrency(subtotal);

        return subtotal;
    }

    function calculateTotals() {
        var total = 0;
        document.querySelectorAll('.receipt-detail-row').forEach(function(row) {
            total += calculateSubtotal(row);
        });

        document.getElementById('total-amount-input').value = total;
        document.getElementById('total-amount-display').textContent = formatCurrency(total) + ' đ';
    }

    // Định dạng tiền tệ
    function formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN').format(amount);
    }

    // Cập nhật giá khi chọn sản phẩm
    function attachProductSelectListener(select) {
        select.addEventListener('change', function() {
            var row = this.closest('.receipt-detail-row');
            var option = this.options[this.selectedIndex];
            var price = option.dataset.price || 0;
            var stock = option.dataset.stock || 0;

            // Cập nhật giá và kiểm tra tồn kho
            row.querySelector('.price-input').value = price;

            var quantityInput = row.querySelector('.quantity-input');
            quantityInput.setAttribute('max', stock);

            calculateSubtotal(row);
            calculateTotals();
        });
    }

    // Cập nhật thành tiền khi thay đổi số lượng hoặc đơn giá
    function attachInputListeners(row) {
        row.querySelectorAll('.quantity-input, .price-input').forEach(function(input) {
            input.addEventListener('input', function() {
                // Kiểm tra số lượng không vượt quá tồn kho
                if (this.classList.contains('quantity-input')) {
                    var select = row.querySelector('.product-select');
                    var option = select.options[select.selectedIndex];
                    var stock = parseInt(option.dataset.stock || 0);

                    if (parseInt(this.value) > stock) {
                        alert('Số lượng xuất không thể vượt quá tồn kho!');
                        this.value = stock;
                    }
                }

                calculateSubtotal(row);
                calculateTotals();
            });
        });
    }

    // Gắn các sự kiện cho tất cả các dòng
    function attachEventListeners() {
        document.querySelectorAll('.receipt-detail-row').forEach(function(row) {
            attachRemoveListener(row.querySelector('.remove-detail'));
            attachProductSelectListener(row.querySelector('.product-select'));
            attachInputListeners(row);
        });
    }

    // Khởi tạo ban đầu
    attachEventListeners();
    calculateTotals();
});
