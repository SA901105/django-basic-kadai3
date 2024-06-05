from django.db import models
from django.conf import settings

# 店舗カテゴリ
class Category(models.Model):
    category_l = models.CharField("業態カテゴリ", max_length=10, blank=False)
    name = models.CharField("業態名", max_length=30, blank=False)

    def __str__(self):
        return str(self.name)

SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

# 店舗情報
class Shop(models.Model):
    name = models.CharField("店舗名", max_length=255)
    pr_long = models.TextField("店舗紹介", blank=True, null=True)
    price_range = models.CharField("予算", max_length=100, blank=True, null=True)
    address = models.CharField("住所", max_length=255, blank=True, null=True)
    tel = models.CharField("TEL", max_length=255, blank=True, null=True)
    opening_hours = models.CharField("営業時間", max_length=255, blank=True, null=True)
    regular_holiday = models.CharField("定休日", max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="カテゴリ")
    description = models.TextField() # description フィールドを追加

    def __str__(self):
        return self.name

# レビュー
class Review(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    comment = models.TextField(verbose_name='レビューコメント', blank=False)
    score = models.PositiveSmallIntegerField(verbose_name='レビュースコア', choices=SCORE_CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('shop', 'user')

    def __str__(self):
        return f'{self.shop.name} - {self.user.username}'

    def get_percent(self):
        percent = round(self.score / 5 * 100)
        return percent

# サブスクリプション　カード支払い
class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255) 
    stripe_subscription_id = models.CharField(max_length=255) 
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

# 店舗予約
class Reservation(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField("予約日時")
    num_people = models.PositiveIntegerField("人数")

    def __str__(self):
        return f'{self.shop.name} - {self.user.username} - {self.datetime}'

class Favorite(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.shop.name} - {self.user.username}'
