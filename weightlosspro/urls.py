"""
URL configuration for weightlosspro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from weighttracker import views





urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_weight, name='add_weight'),
    path('', views.weight_list, name='weight_list'),
    path('edit/<int:pk>/', views.edit_weight, name='edit_weight'),
    path('delete/<int:pk>/', views.delete_weight, name='delete_weight'),
    path('compare_weight/', views.compare_weight ,name='compare_weight')
]

