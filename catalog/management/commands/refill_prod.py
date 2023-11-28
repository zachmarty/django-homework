from typing import Any
from django.core.management import BaseCommand
from catalog.models import Product, Category
import psycopg2

class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        Product.objects.all().delete()
        settings = {
            'user':'postgres',
            'host':'localhost',
            'password':1,
            'dbname':'project5'
        }
        conn = psycopg2.connect(**settings)
        cur = conn.cursor()
        cur.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1")
        conn.commit()
        cur.close()
        conn.close()
        cat = Category.objects.get(id=1)
        product_list = [
            {'name':'test', 'description':'test', 'price':10, 'category':cat},
            {'name':'test', 'description':'test', 'price':10, 'category':cat},
            {'name':'test', 'description':'test', 'price':10, 'category':cat},
            {'name':'test', 'description':'test', 'price':10, 'category':cat},
            {'name':'test', 'description':'test', 'price':10, 'category':cat},
            {'name':'test', 'description':'test', 'price':10, 'category':cat},
            {'name':'test', 'description':'test', 'price':10, 'category':cat},
        ]
        product_for_create = []
        for item in product_list:
            product_for_create.append(Product(**item))
        
        Product.objects.bulk_create(product_for_create)
        print('ok')