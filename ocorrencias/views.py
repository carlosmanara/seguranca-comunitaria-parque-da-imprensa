from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FiltroHistoricoForm, OcorrenciaForm
from .models import Ocorrencia


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


@login_required
def historico(request):
    form = FiltroHistoricoForm(request.GET or None)
    ocorrencias = Ocorrencia.objects.select_related("tipo")

    # RF04: filtros por rua, período e tipo, isolados ou combinados.
    if form.is_valid():
        filtros = form.cleaned_data
        if filtros["rua"]:
            ocorrencias = ocorrencias.filter(rua__icontains=filtros["rua"])
        if filtros["data_inicial"]:
            ocorrencias = ocorrencias.filter(data_hora__date__gte=filtros["data_inicial"])
        if filtros["data_final"]:
            ocorrencias = ocorrencias.filter(data_hora__date__lte=filtros["data_final"])
        if filtros["tipo"]:
            ocorrencias = ocorrencias.filter(tipo=filtros["tipo"])

    contexto = {"form": form, "ocorrencias": ocorrencias}
    return render(request, "ocorrencias/historico.html", contexto)