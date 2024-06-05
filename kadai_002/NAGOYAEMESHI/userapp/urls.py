from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import (
    IndexView, SignUp, Login, Search,
    SubscriptionView, stripe_webhook, MyPageView, ProfileView,
    ReservationsView, FavoritesView, PaymentMethodView, CancelSubscriptionView,
    ShopInfoView, ProfileEditView, ReservationCancelView,  # <- ReservationCancelView を追加
    unfavorite_shop
)

app_name = 'userapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', Search, name='search'),
    path('shop_info/<int:shop_id>/', ShopInfoView.as_view(), name='shop_info'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('mypage/', MyPageView.as_view(), name='mypage'),
    path('mypage/profile/', ProfileView.as_view(), name='profile'),
    path('mypage/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('mypage/reservations/', ReservationsView.as_view(), name='reservations'),
    path('mypage/reservations/cancel/<int:pk>/', ReservationCancelView.as_view(), name='reservation_cancel'),  # <- 予約キャンセル用のURLパターンを追加
    path('mypage/favorites/', FavoritesView.as_view(), name='favorites'),
    path('mypage/favorites/unfavorite/<int:shop_id>/', unfavorite_shop, name='unfavorite_shop'),  # <- お気に入り解除用のURLパターンを追加
    path('mypage/payment_method/', PaymentMethodView.as_view(), name='payment_method'),
    path('mypage/cancel_subscription/', CancelSubscriptionView.as_view(), name='cancel_subscription'),

    # パスワードリセット関連のURLパターンを追加
    path('password_reset/', PasswordResetView.as_view(template_name='userapp/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='userapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='userapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='userapp/password_reset_complete.html'), name='password_reset_complete'),
]
