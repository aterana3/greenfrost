from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from apps.billing.models import Invoice, InvoiceDetail
from apps.products.models import Product
from apps.shopping_cart.models import Cart, CartItem
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class InvoiceCreateView(View):
    def post(self, request):
        data = request.POST

        try:
            user_id = data.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            subtotal = data.get('subtotal')
            tax = data.get('tax')
            total = data.get('total')

            # Crear la factura
            invoice = Invoice.objects.create(
                user=user,
                subtotal=subtotal,
                tax=tax,
                total=total
            )

            # Agregar los detalles de los productos a la factura
            products_data = json.loads(data.get('products'))
            for product_id, product_info in products_data.items():
                product = get_object_or_404(Product, pk=product_id)
                price = product_info['price']
                amount = product_info['amount']
                detail_subtotal = price * amount

                InvoiceDetail.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=amount,
                    price=price,
                    subtotal=detail_subtotal
                )

            # Vaciar el carrito del usuario
            cart = Cart.objects.get(user=user)
            CartItem.objects.filter(cart=cart).delete()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)