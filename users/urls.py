from django.urls import path
from . import views

urlpatterns = [
    path("me", views.MeView.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path('update', views.UpdateMeView.as_view(),),
]
