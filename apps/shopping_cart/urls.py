from django.urls import path
from apps.shopping_cart.views.shopping_cart import AddToCartView, RemoveFromCartView, CartDetailView

app_name = 'shopping_cart'

urlpatterns = [
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]