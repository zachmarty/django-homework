from django.db import models

NULLABLE = {'blank': True, 'null': True}
NOTNULL = {'blank': False, 'null': False}
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', blank=False, null=False)
    description = models.TextField(max_length=1000, verbose_name='Описание', **NULLABLE)

    def __str__(self) -> str:
        return f'{self.id} {self.name}'
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', blank=False, null=False)
    description = models.TextField(max_length=1000, verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='products_images/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Категория')
    price = models.FloatField(blank=False, null=False, verbose_name='Цена')
    created_date = models.DateTimeField(auto_created=True, auto_now=True, blank=False, null=False, verbose_name='Добавлено')
    last_fix_date = models.DateField(auto_now=True, null=False, blank=False, verbose_name='Изменено')

    def __str__(self) -> str:
        return f'{self.id} {self.name} {self.price} {self.category}' 
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)