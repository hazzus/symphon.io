from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index),
    path('about/', TemplateView.as_view(template_name="about.html")),
    path('recognize', views.recognize),
    path('composer/<int:composer_id>/', views.composer, name='composer'),
    path('composers', views.composers, name='composers'),
    path('composer/<int:composer_id>/affiche/', views.affiche),
]
