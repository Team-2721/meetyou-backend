from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomListView.as_view()),
    path("<int:pk>", views.RoomDetailView.as_view()),
    path("search", views.RoomSearchView.as_view()),
]
