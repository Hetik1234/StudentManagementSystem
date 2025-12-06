"""URL routes for smsapp views."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("delete/<str:student_id>/", views.delete, name="delete"),
    path("update/<str:student_id>/", views.update, name="update"),
]
