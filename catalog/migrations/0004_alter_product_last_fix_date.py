# Generated by Django 4.2.7 on 2023-11-29 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='last_fix_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Изменено'),
        ),
    ]
