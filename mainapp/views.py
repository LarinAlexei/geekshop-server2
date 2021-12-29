import json
import os.path

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product

# Create your views here.

links_menu = [
    {'href': 'products_all', 'name': 'Все'},
    {'href': 'products_home', 'name': 'Дом'},
    {'href': 'products_office', 'name': 'Офис'},
    {'href': 'products_modern', 'name': 'Модерн'},
    {'href': 'products_classic', 'name': 'Классика'},
]

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


def products(request, pk=None):
    print(pk)
    # file_path = os.path.join(module_dir, 'json/products.json')
    # products = json.load(open(file_path, encoding='utf-8'))

    title = 'Продукты'

    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': title,
            'links_menu': links_menu,
            'main_menu': main_menu,
            'products': products,
            'category': category,
            'basket': basket,
        }
        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()[:5]

    content = {
        'title': title,
        'links_menu': links_menu,
        'main_menu': main_menu,
        'same_products': same_products,
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
