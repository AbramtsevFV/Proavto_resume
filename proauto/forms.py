from django import forms
from django.forms import Textarea, TextInput
from captcha.fields import CaptchaField
from django.forms import ModelForm
from .models import *


class Search (forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Поиск по сайту'}))

class FeedbackForm(ModelForm):
    # добавляем капчу
    captcha = CaptchaField()
    class Meta:

        model = Feedback
        fields = ['name','title', 'email','massage']
        widgets = {'name': TextInput(attrs={'class': "form-control",
                                            'placeholder': 'Имя'}),
                    'title': TextInput(attrs={'class': "form-control",
                                            'placeholder': 'Тема'}),
                    'email': TextInput(attrs={'class': "form-control",
                                            'placeholder': 'Email'}),
                   'massage': Textarea(attrs={'class': "form-control",
                                            'placeholder': 'Ввидите ваше сообщение'})
                   }