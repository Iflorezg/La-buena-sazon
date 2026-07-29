from django import forms
from .models import Account

class AccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", min_length=6)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña", min_length=6)

    class Meta:
        model = Account
        fields = ('username', 'email', 'phone', 'address', 'city', 'password')

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if phone and len(phone) < 7:
            raise forms.ValidationError("El teléfono es demasiado corto.")
        return phone

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
