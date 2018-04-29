from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/', include('social_network.urls')),
]
