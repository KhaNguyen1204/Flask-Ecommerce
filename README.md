# Ứng dụng Quản Lý Bán Thiết Bị Điện Tử

## Giới thiệu
Đây là một trang web quản lý bán thiết bị điện tử, hỗ trợ các nghiệp vụ quản lý sản phẩm, đơn hàng, khách hàng, kho hàng và kế toán. Ứng dụng hướng tới việc tối ưu hóa quy trình bán hàng, quản lý tồn kho và nâng cao trải nghiệm khách hàng cho các cửa hàng kinh doanh thiết bị điện tử.

## Tính năng chính
- **Quản lý sản phẩm:** Thêm, sửa, xóa, tìm kiếm và phân loại các thiết bị điện tử với thông tin chi tiết và hình ảnh.
- **Quản lý đơn hàng:** Tạo, cập nhật, theo dõi trạng thái đơn hàng, lịch sử mua hàng của khách.
- **Quản lý khách hàng:** Lưu trữ thông tin, lịch sử giao dịch, hỗ trợ chăm sóc khách hàng.
- **Quản lý kho:** Theo dõi tồn kho, nhập/xuất hàng, cảnh báo khi sắp hết hàng.
- **Kế toán:** Quản lý hóa đơn, thanh toán, báo cáo doanh thu, chi phí.
- **Phân quyền người dùng:** Hệ thống phân quyền cho quản trị viên, nhân viên bán hàng, nhân viên kho, nhân viên kế toán và khách hàng.
- **Giao diện thân thiện:** Thiết kế responsive, dễ sử dụng trên mọi thiết bị.
- **Thông báo:** Cập nhật trạng thái đơn hàng, cảnh báo tồn kho, thông báo hệ thống.

## Công nghệ sử dụng
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (Vanilla JS)
- **Cơ sở dữ liệu:** SQLAlchemy (MySQL hoặc các hệ quản trị CSDL khác)
- **Template Engine:** Jinja2
- **Quản lý migration:** Alembic

## Cấu trúc dự án
```
shop/
    __init__.py
    models.py
    decorators.py
    accounting/
    admin/
    carts/
    customers/
    products/
    sale/
    warehouse/
    static/
        css/
        js/
        images/
    templates/
        ...
main.py
requirements.txt
README.md
```

## Hướng dẫn cài đặt
1. **Clone dự án:**
   ```bash
   git clone <repository-url>
   cd Flask-Ecommerce
   ```
2. **Tạo môi trường ảo:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Khởi tạo cơ sở dữ liệu:**
   ```bash
   flask db upgrade
   ```
5. **Chạy ứng dụng:**
   ```bash
   flask run
   ```
6. **Truy cập:**
   Mở trình duyệt và truy cập `http://127.0.0.1:5000/`

## Hướng dẫn sử dụng
### 1. Đăng nhập/Đăng ký
- Người dùng có thể đăng ký tài khoản mới hoặc đăng nhập bằng tài khoản đã có.
- Hệ thống phân quyền: Quản trị viên, nhân viên bán hàng, nhân viên kho, nhân viên kế toán, khách hàng.

### 2. Quản trị viên
- Quản lý người dùng: Thêm, sửa, xóa tài khoản nhân viên và khách hàng.
- Quản lý sản phẩm: Thêm mới, chỉnh sửa, xóa, cập nhật thông tin sản phẩm.
- Xem báo cáo doanh thu, thống kê đơn hàng, quản lý hệ thống.

### 3. Nhân viên bán hàng
- Tạo mới đơn hàng cho khách, cập nhật trạng thái đơn hàng.
- Quản lý danh sách khách hàng, xem lịch sử mua hàng.
- Tìm kiếm, lọc sản phẩm để tư vấn khách hàng.

### 4. Nhân viên kho
- Quản lý nhập/xuất kho, cập nhật số lượng tồn kho.
- Theo dõi cảnh báo khi sản phẩm sắp hết hàng.
- Xem lịch sử nhập/xuất kho.

### 5. Nhân viên kế toán
- Quản lý hóa đơn bán hàng, hóa đơn nhập kho.
- Theo dõi, xác nhận và cập nhật trạng thái thanh toán các đơn hàng.
- Xem, xuất báo cáo doanh thu, chi phí, lợi nhuận.

### 6. Khách hàng
- Duyệt, tìm kiếm, lọc sản phẩm theo danh mục, thương hiệu.
- Xem chi tiết sản phẩm, thêm vào giỏ hàng, đặt hàng trực tuyến.
- Theo dõi trạng thái đơn hàng, xem lịch sử mua hàng.
- Cập nhật thông tin cá nhân, đổi mật khẩu.

### 7. Các chức năng khác
- Nhận thông báo về trạng thái đơn hàng, khuyến mãi, cảnh báo tồn kho.
- Hỗ trợ liên hệ, gửi phản hồi qua trang liên hệ.

## Thành viên nhóm
- Phạm Anh Kiệt
- Lương Văn Duy
- Nguyễn Hà Vũ Kha

## Đóng góp
Chào mừng mọi đóng góp! Hãy fork repository và gửi pull request để được xem xét.

## Giấy phép
Dự án được phát hành theo giấy phép MIT.

## Liên hệ
Mọi thắc mắc hoặc hỗ trợ, vui lòng liên hệ qua GitHub Issues.
