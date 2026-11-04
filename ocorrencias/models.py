from django.db import models


class TipoOcorrencia(models.Model):
    nome = models.CharField(max_length=60, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "tipo de ocorrência"
        verbose_name_plural = "tipos de ocorrência"

    def __str__(self):
        return self.nome


class Ocorrencia(models.Model):
    rua = models.CharField(max_length=120)
    ponto_referencia = models.CharField(max_length=120, blank=True)
    data_hora = models.DateTimeField()
    descricao = models.TextField(max_length=500, blank=True)
    tipo = models.ForeignKey(
        TipoOcorrencia,
        on_delete=models.PROTECT,
        related_name="ocorrencias",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_hora"]
        verbose_name = "ocorrência"
        verbose_name_plural = "ocorrências"

    def __str__(self):
        return f"{self.tipo} em {self.rua} ({self.data_hora:%d/%m/%Y %H:%M})"