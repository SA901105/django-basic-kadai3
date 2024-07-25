# Djangoの管理画面の登録に必要なモジュールをインポート
from django.contrib import admin
# 管理画面に登録するモデルをインポート
from .models import Category, Review, Shop, Subscription

# カテゴリモデルの管理画面設定
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 一覧表示の際に表示するフィールド
    list_display = ('category_l', 'name')
    # 詳細編集画面へのリンクを設定するフィールド
    list_display_links = ('category_l',)
    # 一覧画面で編集可能にするフィールド
    list_editable = ('name',)

# レビューモデルの管理画面設定
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # 一覧表示の際に表示するフィールド
    list_display = ('shop', 'user', 'score')
    # 詳細編集画面へのリンクを設定するフィールド
    list_display_links = ('shop',)
    # 一覧画面で編集可能にするフィールド
    list_editable = ('score',)

# 店舗モデルの管理画面設定
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    # 一覧表示の際に表示するフィールド
    list_display = ('name', 'category', 'address', 'price_range')
    # 検索可能なフィールド
    search_fields = ('name', 'address', 'price_range', 'category__name')
    # フィルター可能なフィールド
    list_filter = ('category',)

# サブスクリプションモデルの管理画面設定
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    # 一覧表示の際に表示するフィールド
    list_display = ('user', 'stripe_customer_id', 'stripe_subscription_id', 'active')
    # 詳細編集画面へのリンクを設定するフィールド
    list_display_links = ('user',)
    # 一覧画面で編集可能にするフィールド
    list_editable = ('active',)

