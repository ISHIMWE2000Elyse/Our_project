# from django.urls import path
# from .views import dashboard_home

# urlpatterns = [
#     path('', dashboard_home, name='dashboard_home'),
# ]

from django.urls import path
from .views import (
    dashboard_home, 
    reports_view, 
    generate_production_summary, 
    download_quality_grading, 
    view_order_performance,
    production_orders_view,
    quality_grading_view,
)

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
    path('reports/', reports_view, name='reports'),
    path('reports/generate/', generate_production_summary, name='generate_production_summary'),
    path('reports/download/', download_quality_grading, name='download_quality_grading'),
    path('reports/view/', view_order_performance, name='view_order_performance'),
    path('production-orders/', production_orders_view, name='production_orders'),
    path('quality-grading/', quality_grading_view, name='quality_grading'),

]
