from django.db import migrations

def create_mock_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')

    categories = [
        ('Electronics',),
        ('Books',),
        ('Clothing',),
        ('Home & Kitchen',),
        ('Sports & Outdoors',),
        ('Beauty & Personal Care',),
    ]
    category_objs = {}
    for name, in categories:
        obj, _ = Category.objects.get_or_create(name=name)
        category_objs[name] = obj

    products = [
        # Electronics
        {
            'name': 'Apple iPhone 15 Pro',
            'description': '6.1-inch display, A17 Pro chip, 128GB, Space Black.',
            'price': 999.99,
            'category': category_objs['Electronics'],
            'stock': 25,
            'image': 'products/iphone15pro.jpeg'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'description': '6.8-inch QHD+ display, 200MP camera, 256GB.',
            'price': 1199.99,
            'category': category_objs['Electronics'],
            'stock': 30,
            'image': ''
        },
        {
            'name': 'Sony WH-1000XM5 Headphones',
            'description': 'Industry-leading noise canceling, wireless, 30h battery.',
            'price': 349.99,
            'category': category_objs['Electronics'],
            'stock': 50,
            'image': ''
        },
        # Books
        {
            'name': 'Atomic Habits',
            'description': 'An Easy & Proven Way to Build Good Habits & Break Bad Ones by James Clear.',
            'price': 16.99,
            'category': category_objs['Books'],
            'stock': 100,
            'image': ''
        },
        {
            'name': 'The Lean Startup',
            'description': 'How Today’s Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses by Eric Ries.',
            'price': 21.99,
            'category': category_objs['Books'],
            'stock': 80,
            'image': ''
        },
        # Clothing
        {
            'name': 'Levi’s 501 Original Jeans',
            'description': 'Classic straight fit, durable denim, timeless style.',
            'price': 59.99,
            'category': category_objs['Clothing'],
            'stock': 60,
            'image': ''
        },
        {
            'name': 'Nike Air Force 1',
            'description': 'Iconic style, all-day comfort, white/white.',
            'price': 89.99,
            'category': category_objs['Clothing'],
            'stock': 40,
            'image': ''
        },
        # Home & Kitchen
        {
            'name': 'Instant Pot Duo 7-in-1',
            'description': 'Electric pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, warmer.',
            'price': 99.99,
            'category': category_objs['Home & Kitchen'],
            'stock': 35,
            'image': ''
        },
        {
            'name': 'Dyson V11 Cordless Vacuum',
            'description': 'Powerful suction, lightweight, up to 60 minutes run time.',
            'price': 599.99,
            'category': category_objs['Home & Kitchen'],
            'stock': 20,
            'image': ''
        },
        # Sports & Outdoors
        {
            'name': 'Fitbit Charge 6',
            'description': 'Fitness tracker with heart rate, GPS, sleep tracking.',
            'price': 129.99,
            'category': category_objs['Sports & Outdoors'],
            'stock': 45,
            'image': ''
        },
        {
            'name': 'Wilson Evolution Basketball',
            'description': 'Official size, indoor game ball, superior grip.',
            'price': 64.99,
            'category': category_objs['Sports & Outdoors'],
            'stock': 25,
            'image': ''
        },
        # Beauty & Personal Care
        {
            'name': 'Olaplex No. 3 Hair Perfector',
            'description': 'Repairs and strengthens all hair types.',
            'price': 28.00,
            'category': category_objs['Beauty & Personal Care'],
            'stock': 70,
            'image': ''
        },
        {
            'name': 'Philips Sonicare ProtectiveClean 6100',
            'description': 'Electric toothbrush, pressure sensor, 2-week battery.',
            'price': 99.95,
            'category': category_objs['Beauty & Personal Care'],
            'stock': 30,
            'image': ''
        },
    ]
    for prod in products:
        Product.objects.get_or_create(
            name=prod['name'],
            defaults={
                'description': prod['description'],
                'price': prod['price'],
                'category': prod['category'],
                'stock': prod['stock'],
                'image': prod['image'],
            }
        )

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0005_rename_order_date_order_created_at_order_status_and_more'),
    ]
    operations = [
        migrations.RunPython(create_mock_data),
    ]
