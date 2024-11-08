from django.urls import path
from .views import products, category

app_name = 'products'

urlpatterns = [
    path('', products.ProductListView.as_view(), name='products_list'),
    path('<int:pk>/', products.ProductDetailView.as_view(), name='product_detail'),
    path('api/list/', products.ProductListAPIView.as_view(), name='product_list_api'),
    path('api/<int:pk>/', products.ProductDetailAPIView.as_view(), name='product_detail_api'),
    path('api/list/recommended', products.ProductRecommendAPIView.as_view(), name='product_recommend_api'),
    path('api/list/categories/', category.CategoryListAPIView.as_view(), name='categories_list_api'),
]