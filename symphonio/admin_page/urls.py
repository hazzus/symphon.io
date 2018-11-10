from django.urls import path, include
from . import views

urlpatterns = [
    path('admin_page', views.admin_page, name='admin_page'),
    path('add_photo', views.add_composer_photo, name='add_photo')
]
