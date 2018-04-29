from django.conf.urls import url
from . import views

urlpatterns = [
    #/home/
    url(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^$', views.index, name='index'),
]
