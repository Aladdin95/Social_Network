from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.http import HttpResponse


def home(request):
    url_1 = '/home/'
    html_1 = '<a href="' + url_1 + '">' + 'USERS' + '</a><br>'
    return HttpResponse(html_1)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/', include('social_network.urls')),
    url(r'', home, name='home'),
]
