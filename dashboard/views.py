from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Store.models import Product, Order
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

    # Get or create reports to track last generated time
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
    report.save()  # Updates last_generated timestamp

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="production_summary_{datetime.date.today()}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(3*cm, height - 3*cm, "Production Summary Report")
    c.setFont("Helvetica", 12)
    c.drawString(3*cm, height - 4*cm, f"Generated on: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}")

    y = height - 5*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(3*cm, y, "Order ID")
    c.drawString(6*cm, y, "Product")
    c.drawString(12*cm, y, "Quantity")
    c.drawString(15*cm, y, "Status")
    y -= 1*cm

    c.setFont("Helvetica", 12)
    for order in Order.objects.all():
        c.drawString(3*cm, y, str(order.id))
        c.drawString(6*cm, y, order.product.title)
        c.drawString(12*cm, y, str(order.quantity))
        c.drawString(15*cm, y, order.payment_status)
        y -= 0.8*cm
        if y < 3*cm:
            c.showPage()
            y = height - 3*cm

    c.save()
    return response


# -------------------- DOWNLOAD QUALITY GRADING REPORT PDF --------------------
@login_required
def download_quality_grading(request):
    report, _ = Report.objects.get_or_create(report_type='quality_grading')
    report.save()  # Updates last_generated timestamp

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="quality_grading_{datetime.date.today()}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(3*cm, height - 3*cm, "Quality Grading Report")
    c.setFont("Helvetica", 12)
    c.drawString(3*cm, height - 4*cm, f"Generated on: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}")

    y = height - 5*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(3*cm, y, "Order ID")
    c.drawString(6*cm, y, "Product")
    c.drawString(12*cm, y, "Grade")
    c.drawString(15*cm, y, "Inspector")
    y -= 1*cm

    c.setFont("Helvetica", 12)
    for order in Order.objects.all():
        c.drawString(3*cm, y, str(order.id))
        c.drawString(6*cm, y, order.product.title)
        c.drawString(12*cm, y, getattr(order, 'quality_grade', 'N/A'))
        c.drawString(15*cm, y, getattr(order, 'inspector', 'N/A'))
        y -= 0.8*cm
        if y < 3*cm:
            c.showPage()
            y = height - 3*cm

    c.save()
    return response


# -------------------- VIEW ORDER PERFORMANCE --------------------
@login_required
def view_order_performance(request):
    report, _ = Report.objects.get_or_create(report_type='order_performance')
    report.save()

    orders = Order.objects.all()
    return render(request, 'dashboard/order_performance.html', {'orders': orders})
