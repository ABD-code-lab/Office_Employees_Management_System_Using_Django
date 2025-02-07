from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_emp/', views.add_emp, name='add_emp'),
    path('display_emp/', views.display_emp, name='display_emp'),
    path('delete_emp/', views.delete_emp, name='delete_emp'),
    path('update_emp/', views.update_emp, name='update_emp'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
]
