from django.contrib import admin
from mainapp.models import(Category, Product, Comment,)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)

# Register your models here.
