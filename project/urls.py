from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app_finance import views
from rest_framework.routers import DefaultRouter

# API Views for DRF
from app_finance.views import TransactionListView, ProfileView

# Define router for API endpoints
router = DefaultRouter()

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='finance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.user_delete, name='user_delete'),

    # Landing and Dashboard URLs
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Plaid-related URLs
    path('plaid/sandbox/create/', views.create_sandbox_item, name='create_sandbox_item'),
    path('plaid/fetch/', views.fetch_transactions, name='fetch_transactions'),
    path('plaid/sandbox/', views.plaid_sandbox, name='plaid_sandbox'),

    # API Endpoints RESTfull Django
    path('api/transactions/', TransactionListView.as_view(), name='api_transactions'),
    path('api/profile/', ProfileView.as_view(), name='api_profile'),
]