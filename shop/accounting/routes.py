from datetime import datetime, timedelta
import io
import csv
from flask import Flask, flash ,render_template, request, redirect, url_for, session, make_response
from shop.customers.model import Order
from shop import db, app
from shop.decorators import role_required
from .forms import RevenueReportForm


def calculate_daily_revenue(orders, start_date, end_date):
    delta = end_date - start_date
    stats = {(start_date + timedelta(days=i)).strftime('%Y-%m-%d'): {'count': 0, 'revenue': 0, 'average': 0.0} for i in range(delta.days + 1)}

    for order in orders:
        date_str = order.date_created.strftime('%Y-%m-%d')
        if date_str in stats:
            stats[date_str]['count'] += 1
            stats[date_str]['revenue'] += order.grand_total

    for date, data in stats.items():
        if data['count'] > 0:
            data['average'] = data['revenue'] / data['count']

    return stats

def calculate_monthly_revenue(orders, start_date, end_date):
    stats = {}

    for order in orders:
        month_str = order.date_created.strftime('%Y-%m')
        if month_str not in stats:
            stats[month_str] = {'count': 0, 'revenue': 0, 'average': 0.0}
        stats[month_str]['count'] += 1
        stats[month_str]['revenue'] += order.grand_total

    for month, data in stats.items():
        if data['count'] > 0:
            data['average'] = data['revenue'] / data['count']

    return stats

def calculate_yearly_revenue(orders, start_date, end_date):
    stats = {}

    for order in orders:
        year_str = order.date_created.strftime('%Y')
        if year_str not in stats:
            stats[year_str] = {'count': 0, 'revenue': 0, 'average': 0.0}
        stats[year_str]['count'] += 1
        stats[year_str]['revenue'] += order.grand_total

    for year, data in stats.items():
        if data['count'] > 0:
            data['average'] = data['revenue'] / data['count']

    return stats

def calculate_summary_revenue(orders, start_date, end_date):
    total_revenue = sum(order.grand_total for order in orders)
    total_orders = len(orders)
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0.0

    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'average_order_value': average_order_value
    }

def get_complete_orders(start_date=None, end_date=None):
    """Retrieve completed orders within a date range."""
    query = Order.query.filter(Order.status == 'completed')
    if start_date and end_date:
        end_date = datetime.combine(end_date, datetime.max.time())
        query = query.filter(Order.date_created.between(start_date, end_date))
    return query.order_by(Order.date_created.desc()).all()

@app.route('/finance_management')
@role_required(['admin', 'accountancy'])
def finance_management():
    form = RevenueReportForm()
    orders = get_complete_orders()
    stats_2025 = calculate_monthly_revenue(
        get_complete_orders(datetime(2025, 1, 1), datetime(2025, 12, 31)),
        datetime(2025, 1, 1), datetime(2025, 12, 31)
    )
    return render_template(
        'accounting/finance_management.html',
        form=form,
        stats=stats_2025,
        report_type='monthly',
        start_time=datetime.now() - timedelta(days=30),
        end_time=datetime.now(),
        orders=orders
    )

@app.route('/revenue_report', methods=['GET', 'POST'])
@role_required(['admin', 'accountancy'])
def revenue_report():
    form = RevenueReportForm()
    orders = []
    stats = None

    if request.method == 'POST' and form.validate():
        start_time = form.start_date.data
        end_time = form.end_date.data
        report_type = form.report_type.data

        orders = get_complete_orders(start_time, end_time)

        if report_type == 'daily':
            stats = calculate_daily_revenue(orders, start_time, end_time)
        elif report_type == 'monthly':
            stats = calculate_monthly_revenue(orders, start_time, end_time)
        elif report_type == 'yearly':
            stats = calculate_yearly_revenue(orders, start_time, end_time)
        else:
            stats = calculate_summary_revenue(orders, start_time, end_time)

        return render_template('accounting/revenue_report.html', form=form, stats=stats, report_type=report_type, start_time=start_time, end_time=end_time, orders=orders)
    # Nếu không có POST, lấy dữ liệu mặc định
    return render_template('accounting/revenue_report.html', form=form)


@app.route('/export_revenue/<start_date>/<end_date>/<report_type>')
@role_required(['accountancy', 'admin'])
def export_revenue(start_date, end_date, report_type):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        # Include the whole end day
        end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

        orders = Order.query.filter(
            Order.date_created.between(start, end),
            Order.status == 'completed'
        ).order_by(Order.date_created.desc()).all()

        # Calculate statistics
        if report_type == 'daily':
            stats = calculate_daily_revenue(orders, start, end)
        elif report_type == 'monthly':
            stats = calculate_monthly_revenue(orders, start, end)
        elif report_type == 'yearly':
            stats = calculate_yearly_revenue(orders, start, end)
        else:
            stats = calculate_summary_revenue(orders, start, end)

        # Prepare CSV with UTF-8 BOM
        output = io.StringIO()
        writer = csv.writer(output)

        # Write statistics
        if report_type in ['daily', 'monthly', 'yearly']:
            writer.writerow(['Loại', 'Số đơn', 'Doanh thu', 'Giá trị TB'])
            for key, data in stats.items():
                writer.writerow([
                    key,
                    data.get('count', 0),
                    data.get('revenue', 0),
                    data.get('average', 0)
                ])
            writer.writerow([])
        else:
            writer.writerow(['Tổng số đơn hàng', stats.get('total_orders', 0)])
            writer.writerow(['Tổng doanh thu', stats.get('total_revenue', 0)])
            writer.writerow(['Giá trị đơn TB', stats.get('average_order_value', 0)])
            writer.writerow([])

        # Write order details
        writer.writerow(['STT', 'Sản phẩm', 'Số lượng', 'Đơn giá', 'Thành tiền', 'Mã đơn hàng', 'Ngày bán'])
        idx = 1
        for order in orders:
            for item in getattr(order, 'order_details', []):
                writer.writerow([
                    idx,
                    getattr(item, 'product_name', ''),
                    getattr(item, 'quantity', ''),
                    getattr(item, 'price', ''),
                    getattr(item, 'subtotal', ''),
                    order.id,
                    order.date_created.strftime('%d/%m/%Y')
                ])
                idx += 1

        # Encode as UTF-8 with BOM for Excel
        csv_data = output.getvalue()
        bom = '\ufeff'
        response = make_response(bom + csv_data)
        response.headers["Content-Disposition"] = f"attachment; filename=revenue_report_{report_type}_{start_date}_{end_date}.csv"
        response.headers["Content-type"] = "text/csv; charset=utf-8"
        return response

    except Exception as e:
        flash(f'Lỗi xuất báo cáo: {str(e)}', 'danger')
        return redirect(url_for('revenue_report'))