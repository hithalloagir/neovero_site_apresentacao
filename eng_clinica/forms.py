from django import forms
from .models import ConsultaOsNew


class GraficoFilterForm(forms.Form):
    # Campo para data de Inicio
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    # Campo para data de Fim
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    # Campo para selecionar Empresa
    empresa = forms.ModelChoiceField(
        queryset=ConsultaOsNew.objects.values_list('empresa', flat=True).distinct(),
        empty_label="Todas as Empresas",
        required=False,
        to_field_name="empresa",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        empresas = ConsultaOsNew.objects.values_list('empresa', flat=True).distinct().order_by('empresa')
        choices = [('', 'Todas as Empresas')] + [(emp, emp) for emp in empresas if emp]
        self.fields['empresa'] = forms.ChoiceField(choices=choices, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
