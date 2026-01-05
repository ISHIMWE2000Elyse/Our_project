from django.urls import path
from .views import signup_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('signup/<int:id>', signup_view, name='signup'),
]
