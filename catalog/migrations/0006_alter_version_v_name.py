# Generated by Django 4.2.7 on 2023-12-19 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='v_name',
            field=models.CharField(default='changed', max_length=100),
        ),
    ]
