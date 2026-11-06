from django import forms
from django.utils import timezone

from .models import Ocorrencia, TipoOcorrencia


class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ["rua", "ponto_referencia", "data_hora", "tipo", "descricao"]
        labels = {
            "rua": "Rua (obrigatório)",
            "ponto_referencia": "Ponto de referência",
            "data_hora": "Data e hora",
            "tipo": "Tipo",
            "descricao": "Descrição",
        }
        widgets = {
            "data_hora": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "descricao": forms.Textarea(attrs={"rows": 3, "maxlength": 500}),
        }
        error_messages = {
            "rua": {"required": "Informe a rua para enviar."},
            "data_hora": {"required": "Informe a data e a hora do fato."},
            "tipo": {"required": "Escolha o tipo da ocorrência."},
            "descricao": {
                "max_length": "A descrição pode ter no máximo 500 caracteres."
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só tipos ativos aparecem no formulário (RF01 e RF05).
        self.fields["tipo"].queryset = TipoOcorrencia.objects.filter(ativo=True)
        self.fields["tipo"].empty_label = "Selecione o tipo"
        self.fields["data_hora"].input_formats = ["%Y-%m-%dT%H:%M", "%d/%m/%Y %H:%M"]

        # Visual do Bootstrap: campos grandes, bons para o toque no celular (RNF04).
        for nome, campo in self.fields.items():
            if nome == "tipo":
                campo.widget.attrs["class"] = "form-select form-select-lg"
            else:
                campo.widget.attrs["class"] = "form-control form-control-lg"

    def clean_data_hora(self):
        # RF02: a data e a hora não podem estar no futuro.
        valor = self.cleaned_data["data_hora"]
        if valor > timezone.now():
            raise forms.ValidationError(
                "A data e a hora não podem ser futuras. Confira e corrija."
            )
        return valor