from django.urls import path

from . import views

urlpatterns = [
    path('', views.indexView, name='indexView'),
    path('<int:orderId>', views.viewOrder, name='viewOrder'),
    path('add', views.addOrder, name='addOrder'),
    path('edit/<int:orderId>', views.editOrder, name='editOrder'),
    path('delete/<int:orderId>', views.deleteOrder, name='deleteOrder'),
]