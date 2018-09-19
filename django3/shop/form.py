from django .forms import Form, ModelForm, widgets
from django.core import validators
from .models import Shop


# class Shop(forms.Form):
#     username = forms.CharField(validators=[validators.RegexValidator('^\d{11}$', message='非法')])
#     age = forms.IntegerField(max_value=100, min_value=18)
#     sex = forms.BooleanField()

#
# class Shop(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField()
#     email = forms.EmailField()

class LoginForm(ModelForm):
    class Meta:
        model = Shop
        fields = ['username', 'password']
        widgets = {
            'username': widgets.TextInput(attrs={'class': 'name_input', 'placeholder': '请输入用户名'}),
            'password': widgets.PasswordInput(attrs={'class': 'pass_input', 'placeholder': '请输入密码'})
        }

#注册


# class RegisterForm(ModelForm):
#     class Meta:
#         model = Shop
#         fields = ['username', 'password', 'email']
#     password2 = forms.CharField(max_length=10, label='确认密码')
