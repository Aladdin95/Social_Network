from . import views
from django.urls import path
from django.conf.urls import include, url


urlpatterns = [
    #/users/
    url(r'reg/$', views.UserFormView.as_view(), name='register'),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^users', views.index, name='index'),
    # url(r'^login', views.login, name='index'),
    url(r'^$', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
]
