from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RegisterUserForm(UserCreationForm):

    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    #UserCreationForm Valida automaticamente
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if (password1 != password2):
            raise form.ValdationError('Senha diferente')
        return password1
        
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        