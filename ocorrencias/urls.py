from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "ocorrencias"

urlpatterns = [
    path("", views.entrada, name="entrada"),
    path("registrar/", views.registrar, name="registrar"),
    path("historico/", views.historico, name="historico"),
    path(
        "entrar/",
        auth_views.LoginView.as_view(template_name="ocorrencias/login.html"),
        name="entrar",
    ),
    path("sair/", auth_views.LogoutView.as_view(), name="sair"),
]