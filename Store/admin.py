from django.contrib import admin
from django.shortcuts import render
from .models import Customer, Address
from .models import Cart
from .models import CartItem

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)