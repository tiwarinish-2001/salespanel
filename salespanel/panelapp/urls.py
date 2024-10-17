from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path("logout/", views.login_view,name="logout"),
    path('sales_dashboard', views.sales_dashboard, name='sales_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('work_history/', views.work_history, name='work_history'),
    path('change_user/', views.change_user, name='change_user'),
    path('scheduled_calls/', views.scheduled_calls, name='scheduled_calls'),
    path('assigned_data/', views.assigned_data, name='assigned_data'),
    path('review_work/', views.review_work, name='review_work'),
    path('userclientinteraction/', views.user_client_interaction, name='user_client_interaction'),
]
