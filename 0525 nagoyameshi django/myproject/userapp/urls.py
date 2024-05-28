from django.urls import path
from .views import StoreListView, StoreDetailView

urlpatterns = [
    path('', StoreListView.as_view(), name='user_store_list'),
    path('<int:pk>/', StoreDetailView.as_view(), name='user_store_detail'),
]
