# Generated by Django 5.0.5 on 2024-08-05 10:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_rename_datetime_reservation_date_time_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('free', '一般ユーザ'), ('payed', '課金ユーザ')], default='free', max_length=20, verbose_name='会員種別')),
                ('username_kana', models.CharField(blank=True, max_length=20, verbose_name='フリガナ')),
                ('post_code', models.CharField(blank=True, max_length=10, verbose_name='郵便番号')),
                ('address', models.CharField(blank=True, max_length=50, verbose_name='住所')),
                ('tel', models.CharField(blank=True, max_length=20, verbose_name='電話番号')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='誕生日')),
                ('business', models.CharField(blank=True, max_length=20, verbose_name='職業')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255)),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=255)),
                ('stripe_card_name', models.CharField(blank=True, max_length=255)),
                ('stripe_setup_intent', models.CharField(blank=True, max_length=255)),
                ('stripe_card_no', models.CharField(blank=True, max_length=20)),
                ('stripe_card_brand', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ')),
            ],
        ),
    ]