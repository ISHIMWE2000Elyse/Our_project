# from django.urls import path
# from .views import dashboard_home

# urlpatterns = [
#     path('', dashboard_home, name='dashboard_home'),
# ]

from django.urls import path
from .views import dashboard_home, reports_view

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
    path('reports/', reports_view, name='reports'),
]
