from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput, modelformset_factory, inlineformset_factory, HiddenInput

from .models import CustomUser, Lessons, LessonsDescriptions, Files


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Type your password'}), help_text=
'''Ваш пароль должен содержать как минимум 8 символов.<br>
Пароль не должен быть слишком простым и распространенным.<br>
Пароль не может состоять только из цифр.''')
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}), help_text='Повторите ваш пароль.')
    class Meta:
        model = CustomUser
        fields = ('email', 'username')
        help_texts = {
            'group': 'Group to which this message belongs to',
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        elif len(password1) < 8:
            raise ValidationError('Длина пароля меньше 8.')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'username', 'is_active', 'is_superuser')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))

class SignUpUserForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}))
    class Meta:
        model = CustomUser
        fields = ('username','email','first_name','last_name', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'}),
            'username': forms.TextInput(attrs={'class': 'input'}),
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'email' : forms.EmailInput(attrs={'class': 'input'}),
            # 'content': forms.TextInput(attrs={'class': 'input'}),
        }

class EditProfile(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('content', 'avatar','first_name','last_name')
        widgets = {
            'content': forms.Textarea(attrs={'class':'ddd textarea-input'}),
            'first_name': forms.TextInput(attrs={'class': 'ddd inline-block'}),
            'last_name': forms.TextInput(attrs={'class': 'ddd inline-block'}),
            'avatar': forms.FileInput(attrs={'class':'ddd'})
        }

class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ('name','speciality','photo')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'ddd'}),
            'speciality': forms.Select(attrs={'class': 'ddd select-class'})
        }

class LessonEdit(forms.ModelForm):
    class Meta:
        model = LessonsDescriptions
        fields = ('topic',)
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'ddd', 'style': 'padding: 10px 15px;'}),
        }

class FileEditForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'i-block m-width-200 ddd', 'style': 'padding: 10px 20px'}),
            'file_type': forms.Select(attrs={'class': 'select-class'}),
        }



SponsorShipsFormSet = inlineformset_factory(LessonsDescriptions, Files, form=FileEditForm, extra=0, can_delete=True, exclude=[])

