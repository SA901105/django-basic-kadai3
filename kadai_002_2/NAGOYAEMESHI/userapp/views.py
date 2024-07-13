from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, View, FormView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Review, Category, Subscription, Shop, Reservation, Favorite
from .forms import SearchForm, SignUpForm, EmailLoginForm, ReviewForm, ReservationForm, ReviewEditForm, SubscriptionForm, ProfileEditForm
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
from django.urls import reverse, reverse_lazy
from .mixins import PaidMemberRequiredMixin

stripe.api_key = settings.STRIPE_SECRET_KEY


# レビュー投稿、お気に入り追加、店舗予約
class ShopInfoView(View):
    template_name = 'userapp/shop_info.html'

    def get(self, request, shop_id):
        return self.render_shop_info(request, shop_id)

    def post(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        if 'review_submit' in request.POST:
            review_form = ReviewForm(data=request.POST)
            if review_form.is_valid():
                existing_review = Review.objects.filter(shop=shop, user=request.user).first()
                if existing_review:
                    messages.error(request, '既にこの店舗にレビューを投稿しています。', extra_tags='review')
                else:
                    review = Review()
                    review.shop = shop
                    review.user = request.user
                    review.score = review_form.cleaned_data['score']
                    review.comment = review_form.cleaned_data['comment']
                    review.save()
                    messages.success(request, 'レビューの投稿が完了しました。', extra_tags='review')
            else:
                messages.error(request, 'レビューの投稿にエラーがあります。', extra_tags='review')
        elif 'reservation_submit' in request.POST:
            reservation_form = ReservationForm(data=request.POST)
            if reservation_form.is_valid():
                reservation = reservation_form.save(commit=False)
                reservation.user = request.user
                reservation.shop = shop
                reservation.save()
                messages.success(request, '予約が完了しました。', extra_tags='reservation')
            else:
                messages.error(request, '予約の投稿にエラーがあります。', extra_tags='reservation')
        elif 'favorite_submit' in request.POST:
            Favorite.objects.create(shop=shop, user=request.user)
            messages.success(request, 'お気に入りに追加しました。', extra_tags='favorite')
        elif 'unfavorite_submit' in request.POST:
            Favorite.objects.filter(shop=shop, user=request.user).delete()
            messages.success(request, 'お気に入りから削除しました。', extra_tags='favorite')

        return redirect('userapp:subscription')

    def render_shop_info(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        review_count = Review.objects.filter(shop=shop).count()
        score_ave = Review.objects.filter(shop=shop).aggregate(Avg('score'))
        average = score_ave['score__avg']
        average_rate = average / 5 * 100 if average else 0
        review_form = ReviewForm()
        review_list = Review.objects.filter(shop=shop)
        reservation_form = ReservationForm(initial={'shop': shop})

        is_favorite = Favorite.objects.filter(shop=shop, user=request.user).exists()

        params = {
            'title': '店舗詳細',
            'review_count': review_count,
            'shop': shop,
            'review_form': review_form,
            'review_list': review_list,
            'average': average,
            'average_rate': average_rate,
            'reservation_form': reservation_form,
            'is_favorite': is_favorite
        }
        return render(request, self.template_name, params)

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
    Shop_info = []

    if request.method == 'GET':
        searchform = SearchForm(request.GET)

        if searchform.is_valid():
            category_id = request.GET.get('category_l', '')
            freeword = request.GET.get('freeword', '')

            if category_id:
                query = Shop.objects.filter(name__icontains=freeword, category_id=category_id)[:10]
            else:
                query = Shop.objects.filter(name__icontains=freeword)[:10]

            total_hit_count = query.count()
            shop_info = query

    params = {
        'total_hit_count': total_hit_count,
        'shop_info': shop_info,
    }

    return render(request, 'userapp/search.html', params)

class ReservationCreateView(LoginRequiredMixin, PaidMemberRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'userapp/reservation_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, '予約が完了しました。', extra_tags='reservation')
        return response

    def get_success_url(self):
        return reverse('userapp:subscription')

class ReservationCancelView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'userapp/reservation_confirm_cancel.html'
    success_url = reverse_lazy('userapp:subscription')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, '予約をキャンセルしました。', extra_tags='reservation')
        return redirect(success_url)

class ReviewEditView(LoginRequiredMixin, PaidMemberRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewEditForm
    template_name = 'userapp/review_form.html'

    def get_success_url(self):
        messages.success(self.request, 'レビューを更新しました。', extra_tags='review')
        return reverse('userapp:subscription')

class ReviewDeleteView(LoginRequiredMixin, PaidMemberRequiredMixin, DeleteView):
    model = Review
    template_name = 'userapp/review_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'レビューを削除しました。', extra_tags='review')
        return reverse('userapp:subscription')

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
                stripe_customer_id='',
                stripe_subscription_id='',
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
        try:
            subscription = Subscription.objects.get(user=self.request.user)
            context['subscription'] = subscription
        except Subscription.DoesNotExist:
            context['subscription'] = None
            messages.error(self.request, 'サブスクリプションが存在しません。')
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
        user = get_user_model().objects.get(email=session['customer_email'])
        subscription = Subscription.objects.get(user=user)
        subscription.stripe_customer_id = session['customer']
        subscription.stripe_subscription_id = session['subscription']
        subscription.active = True
        subscription.save()

    return JsonResponse({'status': 'success'}, status=200)

@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'userapp/profile_edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'プロフィールを更新しました。')
        return reverse('userapp:profile')

class Logout(LogoutView):
    template_name = 'userapp/logout.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/profile.html'

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/mypage.html'

# 新しいビューの追加
class FavoritesView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'userapp/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('shop')

@login_required
def unfavorite_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    Favorite.objects.filter(shop=shop, user=request.user).delete()
    messages.success(request, 'お気に入りから削除しました。', extra_tags='favorite')
    return redirect('userapp:subscription')

class ReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'userapp/reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

class PaymentMethodView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/payment_method.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            subscription = Subscription.objects.get(user=self.request.user)
            context['subscription'] = subscription
        except Subscription.DoesNotExist:
            context['subscription'] = None
            messages.error(self.request, 'サブスクリプションが存在しません。')
        return context

class CancelSubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'userapp/cancel_subscription.html'

    def post(self, request, *args, **kwargs):
<<<<<<< HEAD:kadai_002/NAGOYAEMESHI/userapp/views.py
        subscription = Subscription.objects.get(user=request.user)
        stripe.Subscription.delete(subscription.stripe_subscription_id)
        subscription.active = False
        subscription.save()
        messages.success(request, '有料会員を解約しました。', extra_tags='subscription')
        return redirect('userapp:subscription')
=======
        try:
            subscription = Subscription.objects.get(user=request.user)
            stripe.Subscription.delete(subscription.stripe_subscription_id)
            subscription.active = False
            subscription.save()
            messages.success(request, '有料会員を解約しました。', extra_tags='subscription')
        # except stripe.error.StripeError as e:
            # messages.error(request, f'解約処理に失敗しました: {e.error.message}')
        # except Subscription.DoesNotExist:
            # messages.error(request, 'サブスクリプションが存在しません。')
        except Exception as e:
            messages.error(request, f'予期しないエラーが発生しました: {str(e)}')

        return redirect('userapp:mypage')
>>>>>>> ae9d671 (sabusucription（有料会員）がうまく機能しているかがわかりません):kadai_002_2/NAGOYAEMESHI/userapp/views.py

# 新規作成用
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'userapp/signup.html'

    def form_valid(self, form):
        user = form.save()
        backend = 'django.contrib.auth.backends.ModelBackend'  # ここで適切なバックエンドを指定します
        login(self.request, user, backend=backend)
        return redirect('userapp:index')
