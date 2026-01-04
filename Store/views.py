from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Customer


@login_required
def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'store/product_list.html', {'products': products})


# View product details
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


# Edit product
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.price = request.POST.get('price')
        product.inventory = request.POST.get('inventory')
        product.save()
        return redirect('product_list')  # ✅ FIXED

    return render(request, 'store/product_edit.html', {'product': product})


# Delete product
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')  # ✅ FIXED

@login_required
def product_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')

        Product.objects.create(
            title=title,
            price=price,
            inventory=inventory
        )

        return redirect('product_list')

    return render(request, 'store/product_create.html')
@login_required
def available_products(request):
    products = Product.objects.filter(inventory__gt=0)

    return render(request, 'store/available_products.html', {
        'products': products
    })
@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Prevent ordering out-of-stock products
    if product.inventory <= 0:
        return redirect('available_products')

    # 🔑 Match Customer by email (NOT user)
    try:
        customer = Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        # Optional: redirect or show message
        return redirect('available_products')

    # Create Order
    order = Order.objects.create(
        customer=customer,
        payment_status='P'  # Pending
    )

    # Create Order Item
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=product.price
    )

    # Reduce inventory
    product.inventory -= 1
    product.save()

    return redirect('production_orders')

@login_required
def order_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0 or quantity > product.inventory:
            return redirect('order_quantity', product_id=product.id)

        # Match customer by email
        customer = Customer.objects.get(email=request.user.email)

        # Create Order
        order = Order.objects.create(
            customer=customer,
            payment_status='P'
        )

        # Create Order Item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.price
        )

        # Reduce inventory
        product.inventory -= quantity
        product.save()

        return redirect('production_orders')

    return render(request, 'store/order_quantity.html', {
        'product': product
    })