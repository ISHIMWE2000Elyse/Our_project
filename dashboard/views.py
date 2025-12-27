# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def home(request):
#     apps = [
#         {'name': 'Playground', 'url': '/playground/', 'description': 'Try fun code experiments', 'icon': '🧩'},
#         {'name': 'Store', 'url': '/store/', 'description': 'View and manage products', 'icon': '🛒'},
#         {'name': 'Tags', 'url': '/tags/', 'description': 'Organize content with tags', 'icon': '🏷️'},
#         {'name': 'Likes', 'url': '/likes/', 'description': 'See what users liked', 'icon': '❤️'},
#     ]
#     return render(request, 'dashboard/home.html', {'apps': apps})


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# @login_required
# def dashboard_home(request):
#     return render(request, 'dashboard/home.html')

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# @login_required
# def dashboard_home(request):
#     user = request.user

#     if user.is_superuser:
#         role = 'Admin'
#     elif user.is_staff:
#         role = 'Staff'
#     else:
#         role = 'User'

#     return render(request, 'dashboard/home.html', {
#         'role': role
#     })

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')


@staff_member_required
def reports_view(request):
    return render(request, 'dashboard/reports.html')
