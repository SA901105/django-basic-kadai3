from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review, Category, Subscription
from .forms import SearchForm, SignUpForm, LoginForm, ReviewForm
import json
import requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Avg
from django.contrib import messages
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_keyid():
    return "296f76d7037341ade00e99ce1c5da7bb"

class IndexView(TemplateView):
    template_name = 'userapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        searchform = SearchForm()
        query = get_gnavi_data("", "RSFST09000", "", "花見", 12)
        res_list = rest_search(query)
        pickup_list = extract_restaurant_info(res_list)
        review_list = Review.objects.all()[:10]
        category_list = Category.objects.all()

        context.update({
            'searchform': searchform,
            'pickup_list': pickup_list,
            'review_list': review_list,
            'category_list': category_list
        })

        return context

def Search(request):
    total_hit_count = 0
    restaurants_info = []

    if request.method == 'GET':
        searchform = SearchForm(request.GET)

        if searchform.is_valid():
            category_l = request.GET.get('selected_category', '')
            freeword = request.GET.get('freeword', '')
            query = get_gnavi_data("", category_l, "", freeword, 10)
            res_list = rest_search(query)
            total_hit_count = len(res_list)
            restaurants_info = extract_restaurant_info(res_list)

    params = {
        'total_hit_count': total_hit_count,
        'restaurants_info': restaurants_info,
    }

    return render(request, 'userapp/search.html', params)

def get_gnavi_data(id, category_l, pref, freeword, hit_per_page):
    keyid = get_keyid()
    area = "AREA110"
    query = {
        "keyid": keyid,
        "id": id,
        "area": area,
        "pref": pref,
        "category_l": category_l,
        "hit_per_page": hit_per_page,
        "freeword": freeword
    }
    return query

def rest_search(query):
    res_list = []
    try:
        response = requests.get("https://api.gnavi.co.jp/RestSearchAPI/v3/", params=query)
        response.raise_for_status()
        res = response.json()
        if "error" not in res:
            res_list.extend(res.get("rest", []))
    except requests.exceptions.RequestException as e:
        print(f"HTTPリクエストに失敗しました: {e}")
    except json.JSONDecodeError:
        print("レスポンスのJSONデコードに失敗しました")
    return res_list

def extract_restaurant_info(restaurants):
    restaurant_list = []
    for restaurant in restaurants:
        id = restaurant.get("id")
        name = restaurant.get("name")
        name_kana = restaurant.get("name_kana")
        url = restaurant.get("url")
        url_mobile = restaurant.get("url_mobile")
        shop_image1 = restaurant.get("image_url", {}).get("shop_image1")
        shop_image2 = restaurant.get("image_url", {}).get("shop_image2")
        address = restaurant.get("address")
        tel = restaurant.get("tel")
        station_line = restaurant.get("access", {}).get("line")
        station = restaurant.get("access", {}).get("station")
        latitude = restaurant.get("latitude")
        longitude = restaurant.get("longitude")
        pr_long = restaurant.get("pr", {}).get("pr_long")

        restaurant_list.append([
            id, name, name_kana, url, url_mobile, shop_image1, shop_image2,
            address, tel, station_line, station, latitude, longitude, pr_long
        ])
    return restaurant_list

def ShopInfo(request, restid):
    keyid = get_keyid()
    id = restid
    query = get_gnavi_data(id, "", "", "", 1)
    res_list = rest_search(query)
    restaurants_info = extract_restaurant_info(res_list)
    review_count = Review.objects.filter(shop_id=restid).count()
    score_ave = Review.objects.filter(shop_id=restid).aggregate(Avg('score'))
    average = score_ave['score__avg']
    average_rate = average / 5 * 100 if average else 0

    if request.method == 'GET':
        review_form = ReviewForm()
        review_list = Review.objects.filter(shop_id=restid)
    else:
        form = ReviewForm(data=request.POST)
        score = request.POST['score']
        comment = request.POST['comment']

        if form.is_valid():
            review = Review()
            review.shop_id = restid
            review.shop_name = restaurants_info[0][1]
            review.image_url = restaurants_info[0][5]
            review.user = request.user
            review.score = score
            review.comment = comment
            review.save()
            messages.success(request, 'レビューを投稿しました。')
            return redirect('userapp:shop_info', restid)
        else:
            messages.error(request, 'エラーがあります。')
            return redirect('userapp:shop_info', restid)

    params = {
        'title': '店舗詳細',
        'review_count': review_count,
        'restaurants_info': restaurants_info,
        'review_form': review_form,
        'review_list': review_list,
        'average': average,
        'average_rate': average_rate,
    }

    return render(request, 'userapp/shop_info.html', params)


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'userapp/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            # Stripe Checkout Sessionを作成
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email=user.email,
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            # 一時的にユーザー情報を保存
            Subscription.objects.create(
                user=user,
                stripe_customer_id='',  # ここは後で更新されます
                stripe_subscription_id='',  # ここは後で更新されます
                active=False,
            )
            return redirect(checkout_session.url)
        return render(request, 'userapp/signup.html', {'form': form})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'userapp/login.html'

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('userapp:index')

@method_decorator(login_required, name='dispatch')
class SubscriptionView(TemplateView):
    template_name = 'userapp/subscription.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        subscription = Subscription.objects.get(user=self.request.user)
        context['subscription'] = subscription
        return context

# StripeのWebhookエンドポイントを設定
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'status': 'invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user = User.objects.get(email=session['customer_email'])
        subscription = Subscription.objects.get(user=user)
        subscription.stripe_customer_id = session['customer']
        subscription.stripe_subscription_id = session['subscription']
        subscription.active = True
        subscription.save()

    return JsonResponse({'status': 'success'}, status=200)

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/mypage.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/profile.html'

class ReservationsView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/reservations.html'

class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/favorites.html'

class PaymentMethodView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/payment_method.html'

class CancelSubscriptionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        subscription = Subscription.objects.get(user=request.user)
        stripe.Subscription.delete(subscription.stripe_subscription_id)
        subscription.active = False
        subscription.save()
        return redirect('userapp:mypage')
