from datetime import date

from django.forms import ModelForm, DateInput, TimeInput, TextInput, IntegerField, DateTimeInput, Textarea, HiddenInput
from django.core.exceptions import ValidationError

from .models import Entry

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'
        widgets = {
            'date': DateTimeInput(),
            'text': Textarea(),
            'author': HiddenInput()
        }