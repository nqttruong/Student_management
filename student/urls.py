from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('student/list/', views.list_student, name='student-list'),
    # path('student/view/', views.view_student, name='student-view'),
    path('student/add/', views.add_student, name='add-student'),
    path('student/edit/<str:slug>/', views.edit_student, name='edit-student'),
    path('student/delete/<str:slug>/', views.delete_student, name='delete-student'),
    path('students/<str:slug>/', views.view_student, name="view_student")
]
