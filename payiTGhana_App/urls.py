
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
import debug_toolbar

urlpatterns = [


   url(r'^dashboard/$',  views.dashboard, name='dashboard'),
   url(r'^client/profile/$',  views.clientProfile, name='clientProfile'),
   url(r'^client/pledge/$',  views.pledge, name='pledge'),
   url(r'^task/match/$',  views.match, name='match'),
   url(r'^client/pledges/$',  views.pledges, name='pledges'),
   url(r'^task/matches/$',  views.matches, name='matches'),
   url(r'^task/bulk/matches/sms$',  views.sendMatchNotification, name='bulknotifications'),
   url(r'^(?P<object_id>[0-9]+)/confirm_match/$',  views.matche_confirmed, name='confirmed_matches'),
   url(r'^(?P<object_id>[0-9]+)/delete_pledge/$',views.delete_pledge, name='delete-pledge'),
   url(r'^(?P<object_id>[0-9]+)/delete_match/$',views.delete_match, name='delete-match'),
   url(r'^task/topup/$',  views.topCoin, name='topup'),
   url(r'^client/transactions/$',  views.clientTransaction, name='transactions'),
]

