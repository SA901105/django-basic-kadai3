from django.shortcuts import render
# from django.views.generic import TemplateView, ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView

#　課題010
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Product

# from django.urls import reverse_lazy

# class TopView(TemplateView):
     # template_name = "top.html"
     
class ProductListView(ListView):
     model = Product
     template_name = 'crud/product_list.html'
     context_object_name = 'products'
     # paginate_by = 3
     
#　課題010   
class ProductDetailView(DetailView):
    model = Product
    template_name = 'crud/product_detail.html'
    context_object_name = 'product'
     
# class ProductCreateView(CreateView):
     # model = Product
     # fields = '__all__'
     
# class ProductUpdateView(UpdateView):
     # model = Product
     # fields = '__all__'
     # template_name_suffix = '_update_form'

# class ProductDeleteView(DeleteView):
     # model = Product
     # success_url = reverse_lazy('list')

