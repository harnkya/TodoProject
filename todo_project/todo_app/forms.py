from django import forms
from .models import Todos, Projects


class ListForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ["title", "description", "finished", "date"]

        widgets = {"user": forms.HiddenInput(), 'project': forms.HiddenInput()}


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ["title", "description"]

        widgets = {"user": forms.HiddenInput()}
