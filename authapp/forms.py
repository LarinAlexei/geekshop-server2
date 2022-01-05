from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import forms
from django.core.validators import validate_image_file_extension
from authapp.models import ShopUser
import re


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']

        if data < 18:
            raise forms.ValidationError('Увы но Вам еще нет 18 лет!')
        return data


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'avatar', 'age', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_control'

    def clean_age(self):
        data = self.cleaned_data['age']

        if data < 18:
            raise forms.ValidationError('Увы но Вам еще нет 18 лет!')
        return data

    # Тут я добавил валидацию по имени, разрешаем ввод имени только латинницей и не менее 2 символов
    # def clean_username(self):
    #    user_in = self.cleaned_data['username']
    #    if len(re.findall(r'[а-яА-Я]', user_in)) != 0:
    #        raise forms.ValidationError("Имя пользователя должно быть введено латинскими буквами!")
    #    if len(user_in) < 3:
    #        raise forms.ValidationError("Имя пользователя не может быть менее трех символов!")
    #    return user_in

#    class ShopUserEditForm(UserChangeForm):
#        class Meta:
#            model = ShopUser
#            fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

#        def __init__(self, *args, **kwargs):
#            super().__init__(*args, **kwargs)
#            for field_name, field in self.fields.items():
#                field.widget.attrs['class'] = 'form-control'
#                field.help_text = ''
#                if field_name == 'password':
#                    field.widget = forms.HiddenInput()

#        def clean_age(self):
#            data = self.cleaned_data['age']
#            if data < 18:
#                raise forms.ValidationError("Увы но Вам еще нет 18 лет!")
#            return