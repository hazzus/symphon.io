"""symphonio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.urls import path, include
from django.conf.urls import url

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('compface.urls')),
    path('', include('admin_page.urls')),
    path('', include('concert_parser.urls')),
    path('auth/', include('authorization.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



def handler404(request, *args, **argv):
    return render(request, '404.html')



def handler500(request, *args, **argv):
    return render(request, '500.html')


# import symphonio.background_jobs

