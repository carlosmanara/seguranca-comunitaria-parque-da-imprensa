from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import OcorrenciaForm


def entrada(request):
    return render(request, "ocorrencias/entrada.html")


def registrar(request):
    if request.method == "POST":
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ocorrência registrada com sucesso.")
            return redirect("ocorrencias:registrar")
    else:
        form = OcorrenciaForm()
    return render(request, "ocorrencias/registro.html", {"form": form})