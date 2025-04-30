"""
URL configuration for task_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.Homepage , name = "home"),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    
    path('dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('add-admin/', views.add_admin_view, name='add_admin'),
    path('view_admins', views.view_admins, name = 'view_admins'),
    path('delete-admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('update-admin/<int:admin_id>/', views.update_admin, name='update_admin'),

    path('add-users/', views.add_users_view, name='add_users'),
    path('view_users/', views.view_users, name = 'view_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),

    path('logout/', views.logout_view, name='logout'),

    path('admin_dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
    path('custom-admin/users/', views.admin_view_users, name='admin_view_users'),    path('add/', views.add_task, name='add_task'),
    path('tasks/', views.view_tasks, name='view_tasks'),
    path('tasks/update/<int:id>/', views.update_task, name='update_task'),  
    path('tasks/delete/<int:id>/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/report/', views.view_task_report, name='task_report'),

    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user-tasks/', views.user_tasks, name='user_tasks'),
    path('user-tasks/update/<int:task_id>/', views.update_user_task, name='update_user_task'),

    path('completion-reports/', views.view_completion_reports, name='completion_reports'),

]
