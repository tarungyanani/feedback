from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutViewAllowGet.as_view(next_page='login'), name='logout'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('feedback/<int:feedback_id>/acknowledge/', views.acknowledge_feedback, name='acknowledge_feedback'),
    path('feedback/<int:feedback_id>/edit/', views.edit_feedback, name='edit_feedback'),
    path('feedback/<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),
    path('feedback/export/<int:employee_id>/', views.export_feedback_pdf, name='export_feedback_pdf'),

]
