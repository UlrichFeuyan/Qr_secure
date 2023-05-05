import os

import qrcode
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from core.settings import MEDIA_ROOT
from utils import SHA256
from .models import Employe
from .forms import EmployeForm


class Home(TemplateView):
    template_name = 'personnel/home.html'


class QrScanner(TemplateView):
    template_name = 'personnel/scanner.html'


class EmployeCreateView(CreateView):
    model = Employe
    form_class = EmployeForm
    template_name = 'personnel/add_employe.html'
    success_url = reverse_lazy('personnel:list_employe')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EmployeListView(ListView):
    model = Employe
    template_name = 'personnel/list_employe.html'  # le template pour afficher la liste des employés
    context_object_name = 'employes'  # le nom de la variable contenant la liste des employés dans le contexte

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(active=True)  # ne récupérer que les employés actifs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Liste des employés'
        return context
