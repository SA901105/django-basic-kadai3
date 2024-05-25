from django.shortcuts import render
from django.views.generic import ListView, DetailView
from crud.models import Store

class StoreListView(ListView):
    model = Store
    template_name = 'userapp/store_list.html'
    context_object_name = 'stores'

class StoreDetailView(DetailView):
    model = Store
    template_name = 'userapp/store_detail.html'
    context_object_name = 'store'
