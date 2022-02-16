from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='Краткое описание продукта', max_length=60, blank=True)
    description = models.TextField(verbose_name='Описание продукта', blank=True)
    price = models.DecimalField(verbose_name='Цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @receiver(pre_save, sender=ProductCategory)
    def update_is_active_on_products(sender, instance, **kwargs):
        if instance.pk:
            if instance.is_active:
                instance.product_set.update(is_active=True)
            else:
                instance.product_set.update(is_active=False)

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')