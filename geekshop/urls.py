"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mainapp.views import index, products, contact, context
from django.conf import settings
from django.conf.urls import include

urlpatterns = [
    # Social auth
    path('', include('social_django.urls', namespace='social')),
    # DebugToolbar
    path('__debug__/', include('debug_toolbar.urls')),
    # Application urls
    # path('admin/', admin.site.urls),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('', index, name="index"),
    path('products/', include("mainapp.urls", namespace='products')),
    path('contact/', contact, name="contact"),
    path('context/', context),
    path('products_all', products, name="products_all"),
    path('products_home', products, name="products_home"),
    path('products_office', products, name="products_office"),
    path('products_modern', products, name="products_modern"),
    path('products_classic', products, name="products_classic"),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('order/', include('ordersapp.urls', namespace='order')),
    path('basket/', include('basketapp.urls', namespace='basket')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
