from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from basketapp.models import Basket
from .forms import OrderItemForm
from .models import Order, OrderItem


# Create your views here.


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


def order_list(request):
    objects = Order.objects.filter(user=request.user)
    return render('ordersapp/order_list.html', context={
        'objects': objects
    })


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')


def get_context_data(self, **kwargs):
    data = super().get_context_data(**kwargs)
    OrderFormSet = inlineformset_factory(Order, OrderItem,
                                         form=OrderItemForm, extra=1)

    if self.request.POST:
        formset = OrderFormSet(self.request.POST)
    else:
        basket_items = Basket.get_items(self.request.user)
        if len(basket_items):
            OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                 form=OrderItemForm, extra=len(basket_items))
            formset = OrderFormSet()
            for form, cart_item in zip(formset.forms, basket_items):
                form.initial['product'] = basket_items.product
                form.initial['quantity'] = basket_items.quantity

            basket_items.delete()
        else:
            formset = OrderFormSet()

    data['orderitems'] = formset
    return data


def form_valid(self, form):
    context = self.get_context_data()
    orderitems = context['orderitems']

    with transaction.atomic():
        form.instance.user = self.request.user
        self.object = form.save()
        if orderitems.is_valid():
            orderitems.instance = self.object
            orderitems.save()

    # удаляем пустой заказ
    if self.object.get_total_cost() == 0:
        self.object.delete()

    return super(OrderItemsCreate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


class OrderRead(DetailView):
    model = Order


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet(instance=self.object)
                basket_items.delete()
            else:
                formset = OrderFormSet(instance=self.object)

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:order_list'))
