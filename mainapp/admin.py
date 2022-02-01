from django.contrib import admin
from mainapp.models import ProductCategory, Product

# Register your models here.


admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',)
    list_editable = ('price', 'quantity',)