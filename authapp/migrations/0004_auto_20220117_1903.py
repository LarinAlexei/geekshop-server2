# Generated by Django 3.2.9 on 2022-01-17 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20220115_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveIntegerField(default=18, verbose_name='возраст'),
        ),
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(blank=True, max_length=256, verbose_name='теги')),
                ('about_me', models.TextField(blank=True, max_length=800, verbose_name='о себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Мужчина'), ('F', 'Женщина'), ('X', 'Небинарный')], max_length=1, verbose_name='гендер')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]