from django.urls import path

from . import views

urlpatterns = [
    path('', views.indexView, name='indexView'),
    path('<int:orderId>', views.viewOrder, name='viewOrder'),
]