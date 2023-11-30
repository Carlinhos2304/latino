from django import forms
from .models import Mensaje


class UserLoginForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'loginName',
                'type': 'text',
                'class': 'form-control'
            }
        )
    )

    correo = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'id': 'loginEmail',
                'type': 'email',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'loginPassword',
            'type': 'password',
            'class': 'form-control',
        })
    )


class UserSignUpForm(forms.Form):

    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'id': 'signupNombre',
                'type': 'text',
                'class': 'form-control'
            }
        ))

    correo = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'id': 'signupEmail',
                'type': 'email',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'signupPassword',
                'type': 'password',
                'class': 'form-control'
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control'
            }
        ))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las ContraseÃ±as no coinciden')
        return cd['password2']

#Mensajes administrador

class Messages(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['asunto','mensaje']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a Title'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a Description'}),
        }