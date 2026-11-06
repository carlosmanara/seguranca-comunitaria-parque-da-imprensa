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

class FiltroHistoricoForm(forms.Form):
    rua = forms.CharField(label="Rua", required=False, max_length=120)
    data_inicial = forms.DateField(
        label="Data inicial",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    data_final = forms.DateField(
        label="Data final",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    tipo = forms.ModelChoiceField(
        label="Tipo",
        required=False,
        queryset=TipoOcorrencia.objects.all(),
        empty_label="Todos",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nome, campo in self.fields.items():
            if nome == "tipo":
                campo.widget.attrs["class"] = "form-select form-select-lg"
            else:
                campo.widget.attrs["class"] = "form-control form-control-lg"

    def clean(self):
        dados = super().clean()
        inicial = dados.get("data_inicial")
        final = dados.get("data_final")
        if inicial and final and inicial > final:
            raise forms.ValidationError(
                "A data inicial não pode ser depois da data final. Confira e corrija."
            )
        return dados