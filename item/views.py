from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from store.utils import *
from store.models import Category, Product
from django.core.paginator import Paginator


def products(request):
    data = cookieCart(request)
    data = cartData(request)
    items = data['items']
    cartItems = data['cartItems']
    query = request.GET.get('query', '')

    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    products = Product.objects.filter()

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'products': products,
        'query': query,
        'cartItems': cartItems,
        'categories': categories,
        'items': items,
        'category_id': int(category_id),
        'page_obj': page_obj
    })

def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_items = Product.objects.filter(category=product.category).exclude(pk=pk)[0:3]

    category_id = request.GET.get('category', 0)
    query = request.GET.get('query', '')
    categories = Category.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'product': product,
        'related_items': related_items,
        'items': items,
        'cartItems': cartItems,
        'category_id': int(category_id),
        'categories': categories,


    }
    return render(request, 'item/detail.html', context)
