from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('shop/', views.available_products, name='available_products'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('order/<int:product_id>/quantity/', views.order_quantity, name='order_quantity'),
    path('dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('shop/', views.available_products, name='available_products'),

]
