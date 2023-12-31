# Generated by Django 4.2.7 on 2023-12-06 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_record_creation_date_alter_record_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='attribute',
        ),
        migrations.AddField(
            model_name='record',
            name='dislikes_count',
            field=models.IntegerField(default=0, verbose_name='Дизлайков'),
        ),
        migrations.AddField(
            model_name='record',
            name='likes_count',
            field=models.IntegerField(default=0, verbose_name='Лайков'),
        ),
        migrations.AddField(
            model_name='record',
            name='publicated',
            field=models.BooleanField(default=False, verbose_name='Признак публикации'),
        ),
    ]
