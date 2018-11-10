from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('recognize', views.recognize),
    path('composer/<int:composer_id>/', views.composer, name='composer'),
    path('composers', views.composers, name='composers'),
    path('composer/<int:composer_id>/affiche/', views.affiche)
]
