from django.contrib.auth.models import User, Group

from django.http import HttpResponse
from .models import Client,Pledge
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import account.views
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import ClientUpdate
from django.contrib import messages
from django.shortcuts import get_object_or_404
import uuid
from datetime import datetime
from datetime import timedelta
from django.db.models import Q
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger


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
@login_required
def clientProfile(request):
    current_user = request.user
    if request.method == "POST":
        try:
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

        except:
            messages.error(request, 'Mobile Number or Email already exist')
            return render(request, 'clients/update.html')


    else:
            #client=Client.objects.get(pk=current_user.id)
            try:
                 client=Client.objects.get(user_id=current_user.id)



                 context = {'client': client}

                 return render(request, 'clients/update.html',context )


            except:

                 return render(request, 'clients/update.html')


@login_required
def pledge(request):
    if request.method == "POST":
        maturity= datetime.now() + timedelta(days=10)

        current_user = request.user
        client = Client.objects.get(user_id=current_user.id)


        pledge = Pledge()
        pledge.pledged_amount = request.POST.get('amount')
        pledge.pledge_maker_id= client
        pledge.payment_confirm="Unconfirmed"
        pledge.transaction_code=str(uuid.uuid4())[:8]
        pledge.status=0
        pledge.payment_deadline=timezone.now()
        pledge.repledged=0
        pledge.matched=0
        pledge.payment_deadline=maturity
        pledge.maturity_date=maturity
        pledge.save()
        messages.success(request, 'Pledge created successfully')

        return redirect('pledges')

    else:

        return render(request, 'pledges/make.html')

@login_required
def pledges(request):
    page = request.GET.get('page', 1)
    current_user = request.user
    client = Client.objects.get(user_id=current_user.id)
    data=Pledge.objects.filter(Q(pledge_maker_id=client) | Q(pledge_maker_id=client)).order_by('-id').all()
    paginator = Paginator(data, 50)

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    return render(request, 'pledges/index.html', {'data': records})

@login_required
# def delete_pledge(request):
#     current_user = request.user
#     client = Client.objects.get(user_id=current_user.id)
#     data = Pledge.filter(id=id).filter(pledge_maker_id=current_user.id).delete()
#     messages.success(request, 'Pledge deleted successfully')
#
#     return redirect('pledges')

def delete_pledge(request, object_id):
    object = get_object_or_404(Pledge, pk=object_id)
    object.delete()
    messages.success(request, 'Pledge deleted successfully')

    return redirect('pledges')




