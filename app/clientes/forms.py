from django import forms

from clientes.models import Cliente


class ClienteForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.Textarea())  # ALTERANDO O TAMANHO DA CAIXA DE TEXTO

    class Meta:
        model = Cliente
        fields = ['nome', 'sexo', 'data_nascimento', 'email', 'profissao']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
