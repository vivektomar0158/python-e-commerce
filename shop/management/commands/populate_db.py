from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Populate database with initial categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')
        
        # Define categories with their image paths
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest gadgets and electronics', 'order': 1, 'image': 'categories/electronic.png'},
            {'name': 'Fashion', 'description': 'Trendy clothing and accessories', 'order': 2, 'image': 'categories/fashion.png'},
            {'name': 'Home & Living', 'description': 'Home decor and essentials', 'order': 3, 'image': 'categories/home and living.png'},
            {'name': 'Sports & Fitness', 'description': 'Sports equipment and fitness gear', 'order': 4, 'image': 'categories/sports and fitness.png'},
            {'name': 'Books & Media', 'description': 'Books, magazines, and media', 'order': 5, 'image': 'categories/book and media.png'},
            {'name': 'Beauty & Health', 'description': 'Beauty products and health essentials', 'order': 6, 'image': 'categories/beauty and health.png'},
        ]
        
        # Create categories
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'display_order': cat_data['order'],
                    'image': cat_data['image'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        
        # Define products
        products_data = [
            # Electronics
            {'name': 'Wireless Earbuds Pro', 'category': 'Electronics', 'price': 2499, 'stock': 50, 'description': 'Premium noise-canceling wireless earbuds with crystal clear sound quality and long battery life.', 'image': 'products/Electronics/Screenshot 2026-02-09 224433.png'},
            {'name': 'Smart Laptop Stand', 'category': 'Electronics', 'price': 1299, 'stock': 30, 'description': 'Ergonomic aluminum laptop stand for better posture and improved airflow.', 'image': 'products/Electronics/Screenshot 2026-02-09 224438.png'},
            {'name': 'Gaming Mouse RGB', 'category': 'Electronics', 'price': 899, 'stock': 40, 'description': 'High-precision gaming mouse with customizable RGB lighting and programmable buttons.', 'image': 'products/Electronics/Screenshot 2026-02-09 224444.png'},
            {'name': 'Bluetooth Speaker', 'category': 'Electronics', 'price': 1799, 'stock': 25, 'description': 'Portable waterproof Bluetooth speaker with 360-degree sound and 12-hour battery.', 'image': 'products/Electronics/Screenshot 2026-02-09 224448.png'},
            
            # Fashion
            {'name': 'Summer Straw Hat', 'category': 'Fashion', 'price': 599, 'stock': 35, 'description': 'Elegant wide-brim straw hat perfect for summer outings and beach trips.', 'image': 'products/Fashion/Screenshot 2026-02-09 224457.png'},
            {'name': 'Designer Handbag', 'category': 'Fashion', 'price': 3499, 'stock': 15, 'description': 'Premium leather tote bag with spacious compartments and elegant design.', 'image': 'products/Fashion/Screenshot 2026-02-09 224503.png'},
            {'name': 'Classic Sunglasses', 'category': 'Fashion', 'price': 799, 'stock': 45, 'description': 'UV protection sunglasses with polarized lenses and stylish frames.', 'image': 'products/Fashion/Screenshot 2026-02-09 224507.png'},
            
            # Home & Living
            {'name': 'Scented Candle Set', 'category': 'Home & Living', 'price': 699, 'stock': 60, 'description': 'Set of 3 aromatherapy candles with natural soy wax and essential oils.', 'image': 'products/Home & Living/Screenshot 2026-02-09 224515.png'},
            {'name': 'Decorative Vase', 'category': 'Home & Living', 'price': 1199, 'stock': 20, 'description': 'Modern ceramic vase perfect for fresh or dried flowers.', 'image': 'products/Home & Living/Screenshot 2026-02-09 224518.png'},
            {'name': 'Throw Pillow', 'category': 'Home & Living', 'price': 499, 'stock': 50, 'description': 'Soft cotton cushion with removable cover in various colors.', 'image': 'products/Home & Living/Screenshot 2026-02-09 224522.png'},
            
            # Sports & Fitness
            {'name': 'Yoga Mat Premium', 'category': 'Sports & Fitness', 'price': 1299, 'stock': 40, 'description': 'Non-slip exercise mat with extra cushioning for comfortable workouts.', 'image': 'products/Sports & Fitness/Screenshot 2026-02-09 224537.png'},
            {'name': 'Dumbbell Set', 'category': 'Sports & Fitness', 'price': 2499, 'stock': 15, 'description': 'Adjustable weight dumbbell set for home gym workouts.', 'image': 'products/Sports & Fitness/high-quality-sports-gym-fitness-equipment-sitting-leg-stretcher-fitness-equipment-858.jpg'},
            {'name': 'Resistance Bands', 'category': 'Sports & Fitness', 'price': 599, 'stock': 55, 'description': 'Set of 5 resistance bands for strength training and flexibility.', 'image': 'products/Sports & Fitness/istockphoto-625739874-612x612.jpg'},
            
            # Books & Media
            {'name': 'Media Law Textbook', 'category': 'Books & Media', 'price': 899, 'stock': 25, 'description': 'Comprehensive guide to media law and regulations by Dr. Sukanta K. Nanda.', 'image': 'products/Books & Media/978-81-948080-3-9.jpeg'},
            {'name': 'Fiction Bestseller', 'category': 'Books & Media', 'price': 499, 'stock': 40, 'description': 'Popular fiction novel perfect for book lovers.', 'image': 'products/Books & Media/world-book-day-instagram-template_23-2151963506.avif'},
            {'name': 'Study Guide', 'category': 'Books & Media', 'price': 699, 'stock': 30, 'description': 'Educational resource for students and learners.', 'image': 'products/Books & Media/world-book-day-template-design_23-2151963524.avif'},
            
            # Beauty & Health
            {'name': 'Minimalist Skincare Set', 'category': 'Beauty & Health', 'price': 1999, 'stock': 35, 'description': 'Complete face care routine with cleanser, serum, and moisturizer.', 'image': 'products/Beauty & Health/shopping.webp'},
            {'name': 'Vitamin Serum', 'category': 'Beauty & Health', 'price': 1299, 'stock': 45, 'description': 'Anti-aging vitamin B5 serum for all skin types.', 'image': 'products/Beauty & Health/shopping (1).webp'},
            {'name': 'Face Cleanser', 'category': 'Beauty & Health', 'price': 799, 'stock': 50, 'description': 'Daily cleansing solution with salicylic acid for clear skin.', 'image': 'products/Beauty & Health/Screenshot 2026-02-09 224526.png'},
        ]
        
        # Create products
        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'price': prod_data['price'],
                    'stock_quantity': prod_data['stock'],
                    'description': prod_data['description'],
                    'image': prod_data['image'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
