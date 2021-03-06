"""payiTGhana URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path
import debug_toolbar



urlpatterns = [
    url(r'^admin/', admin.site.urls),
path('', auth_views.login, {'template_name': 'login.html'}, name='login'),
url(r'^logout/$', auth_views.logout, {'next_page': '/auth'}, name='logout'),
    url(r'^auth/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('app/', include('payiTGhana_App.urls')),
    url(r"^account/", include("account.urls")),
url(r"^referrals/", include("pinax.referrals.urls", namespace="pinax_referrals")),

]

urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
