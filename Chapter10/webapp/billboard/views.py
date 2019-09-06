from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader

import datetime

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.models import User
from .models import Bills

from django.conf import settings

def board(request):
    template = loader.get_template('board.html')
    context = {}
    context["isLogged"] = 1

    Bill = Bills.objects.all()

    context["bills"] = Bill

    return HttpResponse(template.render(context, request))

def addbill(request):

    if request.POST:
            billName = request.POST['billname']
            billDesc = request.POST['billdesc']
            Bill = Bills.objects.create(billName=billName, user=request.user, billDesc=billDesc)
            Bill.save()
           
            return redirect('/')
    else:
        template = loader.get_template('add.html')
        context = {}
        context["isLogged"] = 1

        return HttpResponse(template.render(context, request))

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login')
        else:
            template = loader.get_template('login.html')
            context = {}
            return HttpResponse(template.render(context, request))


def logoutView(request):
    logout(request)
    return redirect('/')