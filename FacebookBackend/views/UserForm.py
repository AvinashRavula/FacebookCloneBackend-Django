from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.views.generic.edit import CreateView, UpdateView


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['username', 'email', 'id']
