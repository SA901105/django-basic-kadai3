from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review, Category, Subscription, Shop
from .forms import SearchForm, SignUpForm, EmailLoginForm, ReviewForm
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
from django import forms

stripe.api_key = settings.STRIPE_SECRET_KEY

class IndexView(TemplateView):
    template_name = 'userapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        searchform = SearchForm()
        pickup_list = Shop.objects.all()[:10]
        review_list = Review.objects.select_related('shop').all()[:10]
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
            query = Shop.objects.filter(name__icontains=freeword, category__category_l=category_l)[:10]
            total_hit_count = query.count()
            restaurants_info = query

    params = {
        'total_hit_count': total_hit_count,
        'restaurants_info': restaurants_info,
    }

    return render(request, 'userapp/search.html', params)

class ShopInfoView(View):
    template_name = 'userapp/shop_info.html'

    def get(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        review_count = Review.objects.filter(shop=shop).count()
        score_ave = Review.objects.filter(shop=shop).aggregate(Avg('score'))
        average = score_ave['score__avg']
        average_rate = average / 5 * 100 if average else 0
        review_form = ReviewForm()
        review_list = Review.objects.filter(shop=shop)

        params = {
            'title': '店舗詳細',
            'review_count': review_count,
            'shop': shop,
            'review_form': review_form,
            'review_list': review_list,
            'average': average,
            'average_rate': average_rate,
        }
        return render(request, self.template_name, params)

    def post(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        form = ReviewForm(data=request.POST)
        score = request.POST['score']
        comment = request.POST['comment']

        if form.is_valid():
            review = Review()
            review.shop = shop
            review.user = request.user
            review.score = score
            review.comment = comment
            review.save()
            messages.success(request, 'レビューを投稿しました。')
            return redirect('userapp:shop_info', shop_id=shop_id)
        else:
            messages.error(request, 'エラーがあります。')
            return redirect('userapp:shop_info', shop_id=shop_id)

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
    form_class = EmailLoginForm
    template_name = 'userapp/login.html'

@method_decorator(login_required, name='dispatch')
class SubscriptionView(TemplateView):
    template_name = 'userapp/subscription.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        subscription = Subscription.objects.get(user=self.request.user)
        context['subscription'] = subscription
        return context

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

class CancelSubscriptionForm(forms.Form):
    pass  # 特別なフィールドは不要

@method_decorator(login_required, name='dispatch')
class CancelSubscriptionView(LoginRequiredMixin, FormView):
    template_name = 'userapp/cancel_subscription.html'
    form_class = CancelSubscriptionForm

    def form_valid(self, form):
        subscription = Subscription.objects.get(user=self.request.user)
        stripe.Subscription.delete(subscription.stripe_subscription_id)
        subscription.active = False
        subscription.save()
        messages.success(self.request, '有料プランを解約しました。')
        return redirect('userapp:mypage')

def common_context(request):
    category_list = Category.objects.all()
    return {
        'category_list': category_list,
    }
