
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
import debug_toolbar

urlpatterns = [


   url(r'^dashboard/$',  views.dashboard, name='dashboard'),
   # url(r'^signup/$', views.signup, name='signup'),
   #  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
   #      views.activate, name='activate'),

]
