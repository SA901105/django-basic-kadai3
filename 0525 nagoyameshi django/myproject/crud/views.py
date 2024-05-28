from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Store
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

class TopView(TemplateView):
    template_name = "top.html"

class StoreListView(LoginRequiredMixin, ListView):
    model = Store
    paginate_by = 3
    context_object_name = 'stores'

class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    fields = '__all__'
    template_name = 'crud/store_form.html'

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Store
    fields = '__all__'
    template_name = 'crud/store_update_form.html'

class StoreDeleteView(LoginRequiredMixin, DeleteView):
    model = Store
    success_url = reverse_lazy('store_list')
    template_name = 'crud/store_confirm_delete.html'

class StoreDetailView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = 'crud/store_detail.html'
    context_object_name = 'store'

class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'top.html'
