from django.shortcuts import render

# Create your views here.

links_menu = [
    {'href': 'products_all', 'name': 'Все'},
    {'href': 'products_home', 'name': 'Дом'},
    {'href': 'products_office', 'name': 'Офис'},
    {'href': 'products_modern', 'name': 'Модерн'},
    {'href': 'products_classic', 'name': 'Классика'},
]

menu_main = [
    {'menu_session': 'main', 'name': 'Главная'},
    {'menu_session': 'products', 'name': 'Продукты'},
    {'menu_session': 'contact', 'name': 'Контакты'},
]


def main(request):
    content = {
        'title': 'Главная',
        'menu_main': menu_main
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'menu_main': menu_main,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'menu_main': menu_main
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
