from django.urls import path
from . import views

urlpatterns = [
    path('receive_token/', views.receive_token),
    path('request_token/', views.request_token, name='request_token'),
]
