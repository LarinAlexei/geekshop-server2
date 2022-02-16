import json
import os.path
import random
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from mainapp.models import ProductCategory, Product
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

# Create your views here.


JSON_PATH = 'mainapp/json'


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, \
                                      category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, \
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, \
                                      category__is_active=True).order_by('price')


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
    products = (Product.objects.all().select_related('category')[:3])
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
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')

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


@never_cache
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


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        print('Cработал', type(pk))
        if pk is not None:
            if pk == 0:
                category = {
                    'pk': 0,
                    'name': 'все'
                }
                print('ПК = 0')
                products = get_products_orederd_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_orederd_by_price(pk)

            paginator = Paginator(products, 3)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                'includes/inc_products_list_content.html',
                context=content,
                request=request)
            return JsonResponse({'result': result})
