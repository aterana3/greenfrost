from apps.products.models import Product
import json

def filter_products_keywords(consult):
    keywords = consult.split()
    products = Product.objects.filter(keywords__icontains=keywords[0])
    return products[:5]


def generate_json_response(products):
    return json.dumps([{
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "stock": product.stock,
        "href": '/products/' + str(product.id),
        "categories": [cat.name for cat in products.categories.all()]
    } for product in products])