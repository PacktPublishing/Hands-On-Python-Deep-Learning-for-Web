from django.shortcuts import render, redirect
from django.contrib import messages
import requests


def indexView(request):
    URL = "https://b21588e3.ngrok.io"
    r = requests.get(url=URL)
    data = r.json()
    return render(request, 'index.html', context={'orders': data['orders']})


def viewOrder(request, orderId):
    URL = "https://b21588e3.ngrok.io/" + str(orderId)
    r = requests.get(url=URL)
    data = r.json()
    return render(request, 'view.html', {'order': data['order']})