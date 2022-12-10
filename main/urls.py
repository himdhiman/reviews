from django.urls import path
from main import views

urlpatterns = [
    path("", views.DefaultView.as_view()),
]
