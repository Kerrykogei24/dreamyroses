from django.urls import path

from . import views

app_name = "studio"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("drawings/", views.drawings, name="drawings"),
    path("contact/", views.contact, name="contact"),
]
