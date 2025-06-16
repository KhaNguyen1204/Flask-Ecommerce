document.addEventListener('DOMContentLoaded', function() {
    // Lấy đường dẫn hiện tại
    const currentPath = window.location.pathname;

    // Danh sách các nav item và đường dẫn tương ứng (đã thêm manager_staffs)
    const navItems = {
        '/admin': 'nav-product',
        '/brands': 'nav-brand',
        '/categories': 'nav-category',
        '/manager_customers': 'nav-customer',
        '/manager_staffs': 'nav-staff',  // Thêm đường dẫn quản lý nhân viên
        '/manager_orders': 'nav-order',
        '/warehouse': 'nav-warehouse',
        '/finance_management': 'nav-report',
        '/change_password': 'nav-change-password',
        '/logout': 'nav-logout'
    };

    // Tìm và active nav item tương ứng
    for (const [path, navId] of Object.entries(navItems)) {
        if (currentPath.startsWith(path)) {
            const navElement = document.getElementById(navId);
            if (navElement) {
                navElement.classList.add('active-nav');
                navElement.classList.remove('text-dark');

                // Nếu là dropdown item thì active cả dropdown toggle
                if (navId === 'nav-change-password' || navId === 'nav-logout') {
                    const dropdownToggle = navElement.closest('.dropdown-menu').previousElementSibling;
                    if (dropdownToggle) {
                        dropdownToggle.classList.add('active');
                    }
                }
            }
        }
    }
});
