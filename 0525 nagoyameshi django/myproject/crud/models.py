from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    price = models.PositiveIntegerField(default=0)  # デフォルト値を追加
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(blank=True, default='noImage.png')
    detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    # 新規作成・編集完了時のリダイレクト先
    def get_absolute_url(self):
        return reverse('store_list')
