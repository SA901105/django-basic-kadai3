from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Store, Category
from django.utils.safestring import mark_safe

class NagoyameshiAdminSite(AdminSite):
    site_header = "NAGOYAMESHI 管理サイト"
    site_title = "NAGOYAMESHI 管理サイト"
    index_title = "ようこそNAGOYAMESHI管理サイトへ"

nagoyameshi_admin_site = NagoyameshiAdminSite(name='nagoyameshi_admin')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image')
    search_fields = ('name',)
    list_filter = ('category',)
  
    def image(self, obj):
        return mark_safe('<img src="{}" style="width:100px; height:auto;">'.format(obj.img.url))

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
  
nagoyameshi_admin_site.register(Store, StoreAdmin)
nagoyameshi_admin_site.register(Category, CategoryAdmin)
