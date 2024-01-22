from django import forms
from django.forms import ModelForm
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model= Task
        fields= ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write a description of the task'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
"""
class CreateNewTask(forms.Form):
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    description = forms.CharField(label='Task description',widget=forms.Textarea(attrs={'class': 'input'}))
"""
class CreateNewProyect(forms.Form):
    name = forms.CharField(label='Name of proyect', max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    
