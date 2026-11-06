from django.urls import path

from . import views

app_name = "ocorrencias"

urlpatterns = [
    path("", views.entrada, name="entrada"),
    path("registrar/", views.registrar, name="registrar"),
]