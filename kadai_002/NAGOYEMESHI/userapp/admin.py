from django.contrib import admin
from .models import Category, Review


@admin.register(Category)  
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_l', 'name')
    list_display_links = ('category_l',)
    list_editable = ('name',)
    

@admin.register(Review)  
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('shop_id', 'shop_name', 'user', 'score')
    list_display_links = ('shop_name',)
    list_editable = ('score',)