from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from apps.shopping_cart.models import Cart

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        Cart.objects.get_or_create(user=obj)