from store.models import Product

# Update the iPhone 15 Pro image field to use the correct local path
product = Product.objects.filter(name__icontains='iphone 15 pro').first()
if product:
    product.image = 'products/iphone15pro.jpeg'
    product.save()
    print('Updated iPhone 15 Pro image path to products/iphone15pro.jpeg')
else:
    print('iPhone 15 Pro product not found.')
