from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='Время', auto_now_add=True)

    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         old_basket_item = Basket.objects.get(pk=self.pk)
    #         self.product.quantity = self.quantity - old_basket_item.quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #         self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)

    @classmethod
    def get_items(self, user):
        return Basket.objects.filter(user=user)

    @cached_property
    def items(self):
        return Basket.objects.filter(user=self.user)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.items
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @cached_property
    def total_cost(self):
        _items = self.items.select_related('product')
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost
