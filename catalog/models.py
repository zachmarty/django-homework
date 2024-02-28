from django.db import models
import datetime

from users.models import User

NULLABLE = {"blank": True, "null": True}
# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Наименование", blank=False, null=False
    )
    description = models.TextField(max_length=1000, verbose_name="Описание", **NULLABLE)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Наименование", blank=False, null=False
    )
    description = models.TextField(max_length=1000, verbose_name="Описание", **NULLABLE)
    image = models.ImageField(
        upload_to="products_images/", verbose_name="Изображение", **NULLABLE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Категория",
    )
    price = models.FloatField(blank=False, null=False, verbose_name="Цена")
    created_date = models.DateTimeField(
        auto_created=True,
        auto_now=True,
        blank=False,
        null=False,
        verbose_name="Добавлено",
    )
    last_fix_date = models.DateTimeField(
        auto_now=True, null=False, blank=False, verbose_name="Изменено"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Пользователь",
    )
    publicated = models.BooleanField(default=False, verbose_name="Признак публикации")

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.price} {self.category}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    v_number = models.IntegerField(default=1)
    v_name = models.CharField(max_length=100, default="changed")
    current = models.BooleanField(default=True)
    add_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ("v_name",)
