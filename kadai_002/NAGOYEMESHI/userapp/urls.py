from django.urls import path
from .views import (
    IndexView, SignUp, Login, CustomLogoutView, Search, ShopInfo, 
    SubscriptionView, stripe_webhook, MyPageView, ProfileView, 
    ReservationsView, FavoritesView, PaymentMethodView, CancelSubscriptionView
)

app_name = 'userapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('search/', Search, name='search'),
    path('shop_info/<str:restid>/', ShopInfo, name='shop_info'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('mypage/', MyPageView.as_view(), name='mypage'),
    path('mypage/profile/', ProfileView.as_view(), name='profile'),
    path('mypage/reservations/', ReservationsView.as_view(), name='reservations'),
    path('mypage/favorites/', FavoritesView.as_view(), name='favorites'),
    path('mypage/payment_method/', PaymentMethodView.as_view(), name='payment_method'),
    path('mypage/cancel_subscription/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
]
