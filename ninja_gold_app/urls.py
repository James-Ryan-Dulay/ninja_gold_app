from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('refresh', views.refresh),
    path('process_money', views.process_money)

]