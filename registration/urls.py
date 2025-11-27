from django.urls import path
from . import views

app_name = "registration" 

urlpatterns = [
       # Auth APIs
       path('api/register/', views.register_user, name='register_user'),
       path('api/login/', views.login_api, name='login_api'),
       
       # Expense APIs
       path('api/expenses/', views.expense_list, name='expense_list'),
       path('api/expenses/<int:pk>/', views.expense_detail, name='expense_detail'),
       
       # Existing HTML Views
       path('login/', views.login_view, name='login_html'),
       path('logout/', views.logout_view, name='logout_html'),
       path('users/', views.users_html, name='users_html'),
]