
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
import debug_toolbar

urlpatterns = [


   url(r'^dashboard/$',  views.dashboard, name='dashboard'),
   url(r'^client/profile/$',  views.clientProfile, name='clientProfile')

]

