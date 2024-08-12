from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import datetime
from .forms import *
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib import messages


def store(request):
    data = cookieCart(request)
    data = cartData(request)
    items = data['items']
    cartItems = data['cartItems']
    products = Product.objects.all()
    categories = Category.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    context = {'products': products, 'categories': categories, 'cartItems': cartItems, 'items': items, 'page_obj': page_obj}



    return render(request, 'store/store.html', context)






def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    products = Product.objects.filter()

    if category_id:
        products = products.filter(category_id=category_id)

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'products': products, 'categories': categories,
               'category_id': int(category_id)}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    products = Product.objects.filter()

    if category_id:
        products = products.filter(category_id=category_id)

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'products': products, 'categories': categories,
               'category_id': int(category_id)}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['Action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def signup(request):
    data = cartData(request)
    cartItems = data['cartItems']

    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    products = Product.objects.filter()

    if category_id:
        products = products.filter(category_id=category_id)

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect(request, '/login/', )
    else:

        form = SignupForm()

    return render(request, 'store/signup.html', {
        'form': form,
        'products': products,
        'categories': categories,
        'category_id': int(category_id),
        'cartItems': cartItems
    })
