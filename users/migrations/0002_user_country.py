# Generated by Django 4.2.7 on 2024-02-16 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Страна'),
        ),
    ]