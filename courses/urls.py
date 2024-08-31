# courses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('module/<int:module_id>/complete/', views.mark_module_complete, name='mark_module_complete'),
    path('search/', views.search_courses, name='search_courses'),
]