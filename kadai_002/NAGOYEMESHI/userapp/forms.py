from django import forms
from .models import Category, User, Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SearchForm(forms.Form):
    selected_category = forms.ModelChoiceField(
        label='業態',
        required=False,
        queryset=Category.objects.all(),
    )
    freeword = forms.CharField(min_length=2, max_length=100, label='', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selected_category = self.fields['selected_category']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['score', 'comment']

# サブスクリプション登録
class SubscriptionForm(forms.Form):
    stripe_token = forms.CharField()
