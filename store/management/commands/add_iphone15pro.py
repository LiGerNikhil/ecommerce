from django.core.management.base import BaseCommand
from store.models import Product, Category
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Add iPhone 15 Pro to the database with image'

    def handle(self, *args, **options):
        # Get or create the Electronics category
        category, created = Category.objects.get_or_create(name='Electronics')
        
        # Check if iPhone 15 Pro already exists
        if not Product.objects.filter(name='Apple iPhone 15 Pro').exists():
            # Create the product
            product = Product(
                name='Apple iPhone 15 Pro',
                description='The iPhone 15 Pro features a durable titanium design, A17 Pro chip, and advanced camera system with 48MP Main camera.',
                price=999.99,
                category=category,
                stock=50
            )
            
            # Set the image path
            image_path = os.path.join('products', 'iphone15pro.jpeg')
            full_image_path = os.path.join('media', 'products', 'iphone15pro.jpeg')
            
            # Check if the image file exists
            if os.path.exists(full_image_path):
                with open(full_image_path, 'rb') as img_file:
                    product.image.save('iphone15pro.jpeg', File(img_file), save=False)
                product.save()
                self.stdout.write(self.style.SUCCESS('Successfully added iPhone 15 Pro with image'))
            else:
                # Save without image if file not found
                product.save()
                self.stdout.write(self.style.WARNING('Added iPhone 15 Pro without image (file not found)'))
        else:
            self.stdout.write(self.style.SUCCESS('iPhone 15 Pro already exists in the database'))
