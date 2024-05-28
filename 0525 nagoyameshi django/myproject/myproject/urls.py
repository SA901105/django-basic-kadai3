from django.contrib import admin
from django.urls import path, include
from crud.admin import nagoyameshi_admin_site
from crud import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', nagoyameshi_admin_site.urls),
    path('', views.TopView.as_view(), name="top"),
    path('crud/', views.StoreListView.as_view(), name="store_list"),
    path('user/', include('userapp.urls')),
    path('crud/new/', views.StoreCreateView.as_view(), name="store_create"),  # ここを修正
    path('crud/edit/<int:pk>/', views.StoreUpdateView.as_view(), name="store_edit"),
    path('crud/delete/<int:pk>/', views.StoreDeleteView.as_view(), name="store_delete"),
    path('crud/detail/<int:pk>/', views.StoreDetailView.as_view(), name="store_detail"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
