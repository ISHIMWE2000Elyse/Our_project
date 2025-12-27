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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/home.html')
