from django.urls import path

from . import views

urlpatterns = [
    path("sign-in/", views.sign_in, name="sign_in"),
    path("sign-out/", views.sign_out, name="sign_out"),
    path("me/", views.current_user, name="current_user"),
    path("csrf/", views.csrf_token, name="csrf_token"),
]
