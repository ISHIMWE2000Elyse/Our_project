from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from Store.models import Product, Order, OrderItem
from .models import Report
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


# -------------------- DASHBOARD HOME --------------------
@login_required
def dashboard_home(request):
    products_count = Product.objects.count()
    orders_count = Order.objects.count()

    total_orders = orders_count or 1
    completed_orders = Order.objects.filter(payment_status='C').count()
    grading_rate = int((completed_orders / total_orders) * 100)

    reports_generated = Order.objects.count()

    context = {
        'products_count': products_count,
        'orders_count': orders_count,
        'grading_rate': grading_rate,
        'reports_generated': reports_generated
    }
    return render(request, 'dashboard/home.html', context)


# -------------------- REPORTS VIEW --------------------
@login_required
def reports_view(request):
    products_count = Product.objects.count()
    orders_count = Order.objects.count()

    total_orders = orders_count or 1
    completed_orders = Order.objects.filter(payment_status='C').count()
    grading_rate = int((completed_orders / total_orders) * 100)

    reports_generated = Order.objects.count()

    production_summary, _ = Report.objects.get_or_create(report_type='production_summary')
    quality_grading, _ = Report.objects.get_or_create(report_type='quality_grading')
    order_performance, _ = Report.objects.get_or_create(report_type='order_performance')

    context = {
        'products_count': products_count,
        'orders_count': orders_count,
        'grading_rate': grading_rate,
        'reports_generated': reports_generated,
        'production_summary': production_summary,
        'quality_grading': quality_grading,
        'order_performance': order_performance
    }
    return render(request, 'dashboard/reports.html', context)


# -------------------- GENERATE PRODUCTION SUMMARY PDF --------------------
@login_required
def generate_production_summary(request):
    report, _ = Report.objects.get_or_create(report_type='production_summary')
    report.save()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="production_summary_{datetime.date.today()}.pdf"'
    )

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(3 * cm, height - 3 * cm, "Production Summary Report")

    c.setFont("Helvetica", 12)
    c.drawString(
        3 * cm,
        height - 4 * cm,
        f"Generated on: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}"
    )

    y = height - 5 * cm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Order ID")
    c.drawString(4 * cm, y, "Customer")
    c.drawString(9 * cm, y, "Product")
    c.drawString(14 * cm, y, "Qty")
    y -= 1 * cm

    c.setFont("Helvetica", 11)

    for item in OrderItem.objects.select_related('order', 'product'):
        c.drawString(2 * cm, y, str(item.order.id))
        c.drawString(
            4 * cm,
            y,
            f"{item.order.customer.first_name} {item.order.customer.second_name}"
        )
        c.drawString(9 * cm, y, item.product.title)
        c.drawString(14 * cm, y, str(item.quantity))

        y -= 0.8 * cm
        if y < 3 * cm:
            c.showPage()
            y = height - 3 * cm

    c.save()
    return response


# -------------------- DOWNLOAD QUALITY GRADING REPORT PDF --------------------
@login_required
def download_quality_grading(request):
    report, _ = Report.objects.get_or_create(report_type='quality_grading')
    report.save()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="quality_grading_{datetime.date.today()}.pdf"'
    )

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(3 * cm, height - 3 * cm, "Quality Grading Report")

    c.setFont("Helvetica", 12)
    c.drawString(
        3 * cm,
        height - 4 * cm,
        f"Generated on: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}"
    )

    y = height - 5 * cm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(3 * cm, y, "Order ID")
    c.drawString(7 * cm, y, "Status")
    c.drawString(12 * cm, y, "Grade")
    y -= 1 * cm

    c.setFont("Helvetica", 11)

    for order in Order.objects.all():
        c.drawString(3 * cm, y, str(order.id))
        c.drawString(7 * cm, y, order.get_payment_status_display())
        c.drawString(12 * cm, y, "Auto")  # Placeholder grading
        y -= 0.8 * cm

        if y < 3 * cm:
            c.showPage()
            y = height - 3 * cm

    c.save()
    return response


# -------------------- VIEW ORDER PERFORMANCE --------------------
@login_required
def view_order_performance(request):
    report, _ = Report.objects.get_or_create(report_type='order_performance')
    report.save()

    orders = Order.objects.select_related('customer').all()
    return render(
        request,
        'dashboard/order_performance.html',
        {'orders': orders}
    )
# -------------------- PRODUCTION ORDERS --------------------
@login_required
def production_orders_view(request):
    orders = Order.objects.select_related('customer').all()
    return render(
        request,
        'dashboard/production_orders.html',
        {'orders': orders}
    )