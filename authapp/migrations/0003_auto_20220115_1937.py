# Generated by Django 3.2.9 on 2022-01-15 16:37

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_shopuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activation_expiration_date',
            field=models.DateTimeField(default=authapp.models.default_key_expiration_date, verbose_name='активация истекает'),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(max_length=128, null=True, verbose_name='ключ активации'),
        ),
    ]
