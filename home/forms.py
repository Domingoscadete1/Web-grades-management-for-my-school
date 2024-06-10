from django import forms
from .models import * 

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model=Disciplina
        fields=['nome']

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email
    
