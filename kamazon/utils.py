import re
from django.db.models import Q
from apps.products.models import Product
import json


def filter_products_keywords(consult):
    cleaned_consult = re.sub(r'[^\w\s]', '', consult.lower())
    keywords = cleaned_consult.split()

    query = Q(name__icontains=keywords[0]) | Q(keywords__icontains=keywords[0]) | Q(categories__name__icontains=keywords[0])

    for keyword in keywords[1:]:
        query |= Q(name__icontains=keyword) | Q(keywords__icontains=keyword) | Q(categories__name__icontains=keyword)

    products = Product.objects.filter(query)

    return products[:5]



def generate_json_response(products):
    return json.dumps([{
        "name": product.name,
        "price": float(product.price),
        "description": product.description,
        "stock": product.stock,
        "id": '/products/' + str(product.id),
        "categories": [cat.name for cat in product.categories.all()],
    } for product in products])