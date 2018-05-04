from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('social_network.urls')),
]
