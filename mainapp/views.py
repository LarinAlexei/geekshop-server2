import json
import os.path
import random
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from django.http.response import JsonResponse
from mainapp.models import ProductCategory, Product


# Create your views here.


JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


# links_menu = [
#    {'href': 'products_all', 'name': 'Все'},
#    {'href': 'products_home', 'name': 'Дом'},
#    {'href': 'products_office', 'name': 'Офис'},
#    {'href': 'products_modern', 'name': 'Модерн'},
#    {'href': 'products_classic', 'name': 'Классика'},
# ]

main_menu = [
    {'menu_section': 'index', 'main_urls': 'index', 'name': 'Главная'},
    {'menu_section': 'products:index', 'main_urls': 'products', 'name': 'Продукты'},
    {'menu_section': 'contact', 'main_urls': 'contact', 'name': 'Контакты'},
]

module_dir = os.path.dirname(__file__)


def index(request):
    products = Product.objects.all()[:3]
    content = {
        'title': 'Главная',
        'main_menu': main_menu,
        'products': products,

    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):

    title = 'Продукты'

    # links_menu = ProductCategory.objects.all()
    links_menu = ProductCategory.objects.filter(is_active=True)
    basket = get_basket(request.user)

    # basket = []
#    if request.user.is_authenticated:
#        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            # products = Product.objects.all().order_by('price')
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            # products = Product.objects.filter(category__pk=pk).order_by('price')
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'main_menu': main_menu,
            'products': products_paginator,
            'category': category,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    # same_products = Product.objects.all()[:5]

    content = {
        'title': title,
        'links_menu': links_menu,
        'main_menu': main_menu,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'main_menu': main_menu
    }
    return render(request, 'mainapp/contact.html', content)


def context(request):
    content = {
        'title': 'магазин',
        'header': 'Доброго времени суток',
        'username': 'Ларина Е.В.',
        'products': [
            {'name': 'Стулья', 'price': 4545},
            {'name': 'Диваны', 'price': 9545},
            {'name': 'Кровати', 'price': 9999},
        ]
    }

    return render(request, 'mainapp/test_context.html', content)


def product(request, pk):
    title = 'Продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),

    }

    return render(request, 'mainapp/product.html', content)


def product_price(request, pk):
    products = Product.objects.filter(pk=pk)

    if products:
        return JsonResponse({'price': products[0].price})
    else:
        return JsonResponse({'price': 0})