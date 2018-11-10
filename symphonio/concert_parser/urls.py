from django.urls import path, include
from . import views

urlpatterns = [
    path('parse/', views.parse, name='update')
]