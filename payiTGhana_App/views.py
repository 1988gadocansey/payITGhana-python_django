from django.contrib.auth.models import User, Group

from django.http import HttpResponse
from .models import Client
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import account.views
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
class SignupView(account.views.SignupView):

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

    def update_profile(self, form):
        profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
        profile.some_attr = "some value"
        profile.save()
@login_required
def dashboard(request):
    try:
        department = Client.objects.order_by('created_at')
        context = {'department': department}
    except Client.DoesNotExist:
        raise Http404("Department entity does not exist")
    return render(request, 'dashboard/index.html', context)
def my_view(request):

    # Let's assume that the visitor uses an iPhone...
    request.user_agent.is_mobile # returns True
    request.user_agent.is_tablet # returns False
    request.user_agent.is_touch_capable # returns True
    request.user_agent.is_pc # returns False
    request.user_agent.is_bot # returns False

    # Accessing user agent's browser attributes
    request.user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    request.user_agent.browser.family  # returns 'Mobile Safari'
    request.user_agent.browser.version  # returns (5, 1)
    request.user_agent.browser.version_string   # returns '5.1'

    # Operating System properties
    request.user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
    request.user_agent.os.family  # returns 'iOS'
    request.user_agent.os.version  # returns (5, 1)
    request.user_agent.os.version_string  # returns '5.1'

    # Device properties
    request.user_agent.device  # returns Device(family='iPhone')
    request.user_agent.device.family  # returns 'iPhone'

    return HttpResponse(str(request.user_agent.os ))

def clientProfile(request):
    current_user = request.user

    try:
        client = Client.objects.all().select_related("user_id")[0: 1]
        context = {'data': client}
    except Client.DoesNotExist:
        raise Http404("Client entity does not exist")
    return render(request, 'clients/update.html', context)

