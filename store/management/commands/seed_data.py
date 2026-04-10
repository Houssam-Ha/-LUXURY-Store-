# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from store.models import Product, Review
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Command(BaseCommand):
    help = 'Add seed data for the store'

    def handle(self, **options):
        # Create the main product - Burberry Hoodie
        if not Product.objects.filter(slug='hoodie-burberry-london').exists():
            product = Product.objects.create(
                name="Hoodie Burberry London",
                slug="hoodie-burberry-london",
                description="Luxury men's hoodie from Burberry London, premium quality",
                price=109,
                original_price=130,
                colors=["Light Gray", "Dark Gray", "Blue"],
                sizes=["S", "M", "L", "XL", "XXL"],
                stock=50,
                is_featured=True,
                is_active=True,
            )
            print('Product created successfully')
        else:
            product = Product.objects.get(slug='hoodie-burberry-london')
            print('Product already exists')

        # Create sample reviews
        if not Review.objects.exists():
            reviews_data = [
                {"name": "Mohammed B.", "rating": 5, "comment": "Excellent quality and great price. Fast delivery!"},
                {"name": "Ahmed H.", "rating": 5, "comment": "Luxury fabric and high quality. Highly recommended!"},
                {"name": "Youssef A.", "rating": 5, "comment": "Great customer service. Product matches pictures!"},
                {"name": "Karim S.", "rating": 4, "comment": "Great product, delivery was a bit slow but quality is worth it."},
                {"name": "Rachid K.", "rating": 5, "comment": "Best hoodie I bought, perfect fit and excellent material."},
            ]

            for rev_data in reviews_data:
                Review.objects.create(
                    product=product,
                    customer_name=rev_data["name"],
                    rating=rev_data["rating"],
                    comment=rev_data["comment"],
                    is_approved=True
                )
            print('Reviews created successfully')
        else:
            print('Reviews already exist')

        print('Done!')
