from django.db import models

NULLABLE = {"blank": True, "null": True}


# Create your models here.
class Record(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название", unique=True)
    slug = models.SlugField(verbose_name="Slug", **NULLABLE)
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(**NULLABLE, verbose_name="Картинка")
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    likes_count = models.IntegerField(default=0, verbose_name="количесвто Лайков")
    dislikes_count = models.IntegerField(default=0, verbose_name="количество Дизлайков")
    publicated = models.BooleanField(default=True, verbose_name="Признак публикации")

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ("title",)
