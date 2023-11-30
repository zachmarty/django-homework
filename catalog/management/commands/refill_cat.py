from typing import Any
from django.core.management import BaseCommand
from catalog.models import Category
import psycopg2


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        Category.objects.all().delete()
        settings = {
            "user": "postgres",
            "host": "localhost",
            "password": 1,
            "dbname": "project5",
        }
        conn = psycopg2.connect(**settings)
        cur = conn.cursor()
        cur.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1")
        conn.commit()
        cur.close()
        conn.close()
        category_list = [
            {"name": "test", "description": "test"},
            {"name": "test", "description": "test"},
            {"name": "test", "description": "test"},
            {"name": "test", "description": "test"},
            {"name": "test", "description": "test"},
        ]

        category_for_create = []
        for item in category_list:
            category_for_create.append(Category(**item))

        Category.objects.bulk_create(category_for_create)
        print("ok")
