from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', views.profile, name='profile'),
    path('hr/', views.hr_view, name='hr_view'),
    path('ceo/', views.ceo_view, name='ceo_view'),
    path('manager/', views.manager_view, name='manager_view'),
    path('hiring/', views.hiring_list, name='hiring_list'),
    path('hiring/add/', views.hiring_create, name='hiring_create'),
    path('hiring/<int:pk>/edit/', views.hiring_update, name='hiring_update'),
    path('hiring/<int:hiring_id>/onboard/', views.onboard_employee, name='onboard_employee'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('register/', views.register_view, name='register'),
]