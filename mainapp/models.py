from django.db import models
from django.contrib.auth import get_user_model
from mainapp.config import RAITING, ONE
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name='Имя')
    image = models.ImageField(upload_to='categories/images/', verbose_name= 'Картинка')
    def __str__(self) -> str:
        return self.name
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'   
class Product(models.Model):
    category = models.ForeignKey(to = Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150, verbose_name='Имя продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ценга продукта')
    image = models.ImageField(upload_to='product/images/', verbose_name='Картинка')
    description = models.CharField(max_length=150)
    def __str__(self) -> str:
            return f'Продукт {self.name} от категории {self.category.name}'
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = verbose_name + 'ы'
class Comment(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='comments')
    raiting = models.CharField(max_length = 120,choices=RAITING, default=ONE, verbose_name='Рейтинг')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.CharField(max_length=120, verbose_name='Текст для комментов')
    created_at = models.DateTimeField(auto_now_add=True, null = True, verbose_name='Дата создания')
    def __str__(self) -> str:
         return self.user.username
    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = verbose_name + 'ы'           