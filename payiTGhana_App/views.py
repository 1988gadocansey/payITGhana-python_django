from django.contrib.auth.models import User, Group

from django.http import HttpResponse
from .models import Client
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import account.views
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import ClientUpdate
from django.contrib import messages
from django.shortcuts import get_object_or_404

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
    if request.method == "POST":

            client = Client()
            client.phone= request.POST.get('phone')
            client.firstname=request.POST.get('firstname')
            client.lastname=request.POST.get('lastname')
            client.gender=request.POST.get('gender')
            client.mobile_money_name=request.POST.get('mobile_money_name')
            client.mobile_money_phone=request.POST.get('mobile_money_phone')
            client.user_id = current_user
            client.email = request.POST.get('email')
            client.address = request.POST.get('address')
            client.referrer = request.POST.get('referrer')
            client.date_joined=timezone.now()

            client.save()
            messages.success(request, 'Form submission successful')

            return HttpResponseRedirect('/app/dashboard/')

    else:
            #client=Client.objects.get(pk=current_user.id)
            client=Client.objects.get(user_id=current_user.id)
            context = {'client': client}


            if client:

                return render(request, 'clients/update.html',context )
            else:
                return render(request, 'clients/update.html')





