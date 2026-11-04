from django.contrib import admin

from .models import Ocorrencia, TipoOcorrencia


@admin.register(TipoOcorrencia)
class TipoOcorrenciaAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo")


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ("rua", "tipo", "data_hora")
    list_filter = ("tipo",)