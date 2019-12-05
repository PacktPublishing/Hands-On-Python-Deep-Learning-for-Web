from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm
from django.http import JsonResponse

def indexView(request):
    orders = Order.objects.all()
    orders = list(orders.values())
    return JsonResponse({'orders': orders})

def viewOrder(request, orderId):
    order = Order.objects.filter(id=orderId)
    order = list(order.values())
    return JsonResponse({'order': order})

def addOrder(request):
    if request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            if form.save():
                return JsonResponse('Order created')
            else:
            	return JsonResponse('There was an error')
        else:
            return JsonResponse('Invalid form details')
    else:
        return JsonResponse('Invalid form details')

def editOrder(request, orderId):
    order = Order.objects.get(id=orderId)
    if request.POST:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            if form.save():
                return JsonResponse('Order updated')
            else:
                return JsonResponse('There was an error')
        else:
            return JsonResponse('Invalid form details')
    else:
        return JsonResponse('Invalid form details')

def deleteOrder(request, orderId):
    order = Order.objects.get(id=orderId)
    order.delete()
    return JsonResponse('Order deleted')