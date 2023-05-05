from .models import *
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, DateInput, Select, TextInput, ClearableFileInput


class EmployeForm(ModelForm):
    class Meta:
        model = Employe
        fields = ('name', 'departement', 'poste', 'ncni', 'date_naissance')
        labels = {
            'name': _("Nom"),
            'departement': _("Département"),
            'poste': _("Poste"),
            'ncni': _("Numéro de CNI"),
            'date_naissance': _("Date de Naissance"),
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'employe', 'type': 'text'}),
            'departement': Select(attrs={'class': 'form-control', 'placeholder': 'Département'}),
            'poste': TextInput(attrs={'class': 'form-control', 'placeholder': 'Poste Occupé', 'type': 'text'}),
            'ncni': TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de cni', 'type': 'text'}),
            'date_naissance': DateInput(format=('%d/%m/%Y'),
                                        attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                               'type': 'date', 'min': '1940-01-01', 'max': '2012-12-31'}),
             'photo': ClearableFileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        }


class DepartementForm(ModelForm):
    class Meta:
        model = Departement
        fields = ('name', 'description')
        labels = {
            'name': _("Nom"),
            'description': _("description"),
        }
