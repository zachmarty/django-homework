# Generated by Django 4.2.7 on 2024-02-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_product_publicated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='publicated',
            field=models.BooleanField(default=False, verbose_name='Признак публикации'),
        ),
    ]