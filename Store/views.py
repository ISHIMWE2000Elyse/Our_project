from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product


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
