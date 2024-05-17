from django.db import models
from django.urls import reverse

class Product(models.Model):
  name = models.CharField(max_length=200)
  price = models.PositiveIntegerField()
  description = models.TextField(blank=True, null=True)  # 商品詳細の説明を追加
  category = models.CharField(max_length=255, blank=True, null=True)  # カテゴリを追加
  image = models.ImageField(upload_to='images/', blank=True, null=True)  # 商品画像を追加
  
 
  def __str__(self):
    return self.name

  # 新規作成・編集完了時のリダイレクト先
  def get_absolute_url(self):
    return reverse('list')
