# Generated by Django 3.2.9 on 2022-02-01 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productcategory',
            old_name='descriptions',
            new_name='description',
        ),
    ]
