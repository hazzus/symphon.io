from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('recognize', views.recognize),
    path('composers/<int:composer_id>/', views.composer)
]
