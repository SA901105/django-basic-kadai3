from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import (
    IndexView, SignUpView, Login, Search,
    SubscriptionView, stripe_webhook, MyPageView, ProfileView,
    ReservationsView, FavoritesView, PaymentMethodView, CancelSubscriptionView,
    ShopInfoView, ProfileEditView, ReservationCancelView,
    unfavorite_shop, SubscribeView  # ここにSubscribeViewを追加
)

app_name = 'userapp'

urlpatterns = [
    # ホームページ
    path('', IndexView.as_view(), name='index'),

    # ユーザー登録ページ
    path('signup/', SignUpView.as_view(), name='signup'),

    # ログインページ
    path('login/', Login.as_view(), name='login'),

    # ログアウト
    path('logout/', LogoutView.as_view(), name='logout'),

    # 検索機能
    path('search/', Search, name='search'),

    # 店舗情報ページ
    path('shop_info/<int:shop_id>/', ShopInfoView.as_view(), name='shop_info'),

    # サブスクリプション情報ページ
    path('subscription/', SubscriptionView.as_view(), name='subscription'),

    # StripeのWebhook
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),

    # マイページ
    path('mypage/', MyPageView.as_view(), name='mypage'),

    # プロフィールページ
    path('mypage/profile/', ProfileView.as_view(), name='profile'),

    # プロフィール編集ページ
    path('mypage/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),

    # ユーザーの予約一覧
    path('mypage/reservations/', ReservationsView.as_view(), name='reservations'),

    # 予約キャンセルページ
    path('mypage/reservations/cancel/<int:pk>/', ReservationCancelView.as_view(), name='reservation_cancel'),

    # ユーザーのお気に入り一覧
    path('mypage/favorites/', FavoritesView.as_view(), name='favorites'),

    # お気に入りからの削除
    path('mypage/favorites/unfavorite/<int:shop_id>/', unfavorite_shop, name='unfavorite_shop'),

    # 支払い方法ページ
    path('mypage/payment_method/', PaymentMethodView.as_view(), name='payment_method'),

    # サブスクリプションキャンセルページ
    path('mypage/cancel_subscription/', CancelSubscriptionView.as_view(), name='cancel_subscription'),

    # サブスクリプション登録用のURLパターン
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),

    # パスワードリセット関連のURLパターン
    path('password_reset/', PasswordResetView.as_view(template_name='userapp/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='userapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='userapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='userapp/password_reset_complete.html'), name='password_reset_complete'),
]
