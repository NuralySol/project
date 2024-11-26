"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app_finance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='finance/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
# Add the URL pattern for the fetch_transactions view to fetch transactions from Plaid.
urlpatterns += [
    path('plaid/sandbox/create/', views.create_sandbox_item, name='create_sandbox_item'),
    path('plaid/fetch/', views.fetch_transactions, name='fetch_transactions'),
    path('plaid/sandbox/', views.plaid_sandbox, name='plaid_sandbox'),
]