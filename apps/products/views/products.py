from django.db.models import Q
from django.views.generic import DetailView, ListView
from apps.products.models import Product, Category
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail/page.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'product/list/page.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('categories')
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('search')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = queryset.filter(categories=category)

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.only('id', 'name', 'image')
        context['selected_category'] = self.request.GET.get('category')
        return context


class ProductDetailAPIView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'description': product.description,
            'image': product.get_image(),
        }
        return JsonResponse(data)


class ProductListAPIView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock,
                'description': product.description,
                'image': product.get_image(),
            })
        return JsonResponse(data, safe=False)


class ProductRecommendAPIView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-views')[:3]
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock,
                'description': product.description,
                'image': product.get_image(),
            })
        return JsonResponse(data, safe=False)


class RecentAddedProductListAPIView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-created_at')[:3]
        data = []
        for product in products:
            data.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock,
                'description': product.description,
                'image': product.get_image(),
            })
        return JsonResponse(data, safe=False)