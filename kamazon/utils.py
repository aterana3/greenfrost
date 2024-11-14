import re
from django.db.models import Q
from apps.products.models import Product
import json


def filter_products_keywords(consult):
    cleaned_consult = re.sub(r'[^\w\s]', '', consult.lower().strip())
    keywords = [word for word in cleaned_consult.split() if len(word) > 2]

    if not keywords:
        return Product.objects.none()

    query = Q()
    for keyword in keywords:
        keyword_query = (
                Q(name__icontains=keyword) |
                Q(keywords__icontains=keyword) |
                Q(categories__name__icontains=keyword) |
                Q(description__icontains=keyword)
        )
        query |= keyword_query

    products = Product.objects.filter(query).distinct()
    return products[:5]


def generate_json_response(products):
    return [{
        "id": str(product.id),
        "name": product.name,
        "price": float(product.price),
        "description": product.description,
        "stock": product.stock,
        "categories": [cat.name for cat in product.categories.all()],
    } for product in products]
