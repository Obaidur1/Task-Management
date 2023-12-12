from django.forms import ModelForm, DateField, widgets
from django import forms
from .models import Task
from django.core.exceptions import ValidationError


class TaskEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority", "mark_as_completed"]
        widgets = {"due_date": widgets.DateInput(attrs={"type": "date"})}
