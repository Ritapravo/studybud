"""
URL configuration for studybud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
# from django.http import HttpResponse

# def home(request):
#     # request object is going to be the http object. It tells us about the 
#     # what kind of request is sent, what kind of data is passed in, whats the user sending to the bckend
#     return HttpResponse('Home Page')
# def room(request):
#     return HttpResponse('Room Page')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home),
    # path('room/', room),
    path('', include('base.urls')),
]
