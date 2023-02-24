from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_view, name='register'),

    path('', views.home, name="home"),
    path('project/<str:pk>', views.project, name="project"),
    path('profile/<str:pk>', views.user_profile, name="user-profile"),

    path('create-project/', views.create_project, name="create-project"),
    path('update-project/<str:pk>/', views.update_project, name="update-project"),
    path('delete-project/<str:pk>/', views.delete_project, name="delete-project"),
    path('delete-message/<str:pk>/', views.delete_message, name="delete-message"),
]
