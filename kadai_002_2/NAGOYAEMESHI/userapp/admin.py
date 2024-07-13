# admin.py
from django.contrib import admin
from .models import Category, Review, Shop

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_l', 'name')
    list_display_links = ('category_l',)
    list_editable = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('shop', 'user', 'score')
    list_display_links = ('shop',)
    list_editable = ('score',)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'address', 'price_range')
    search_fields = ('name', 'address', 'price_range', 'category__name')
    list_filter = ('category',)
