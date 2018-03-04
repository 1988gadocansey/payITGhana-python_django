from django.contrib.auth.models import User, Group

from django.http import HttpResponse
from .models import Client,Pledge,Match,Sms,Coins
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
from django.db.models import Count,Sum
from django.db.models import F
import urllib

class SignupView(account.views.SignupView):

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

    def update_profile(self, form):
        profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
        profile.some_attr = "some value"
        profile.save()




def send_sms(phone, message,sender):

    phone="0"+str(phone)
    client = Client.objects.get(user_id=sender)
    sender_id="PayiTGh"
    api_key="4ef55e5f24720b20f1e4"
    # parameters to send SMS
    params = {"key": api_key, "to": phone, "msg": message, "sender_id": sender_id}

    url = 'http://sms.gadeksystems.com/smsapi?' + urllib.parse.urlencode(params)


    content = urllib.request.urlopen(url).read()
    status=""
    # Interpreting codes obtained from reading the URL
    if (content.strip() == '1000'):

         status="Message successfully sent"
         print (status)
    elif (content.strip() == '1002'):

         status="Message not sent"
         print(status)
    elif (content.strip() == '1003'):

         status="Your balance is not enough"
         print(status)
    elif (content.strip() == '1004'):

         status="Invalid API Key"
         print(status)
    elif (content.strip() == '1005'):

         status="Phone number not valid"
         print(status)
    elif (content.strip() == '1006'):

         status="Invalid sender id"
    elif (content.strip() == '1008'):
        status="Empty message"
    print(status)

    sms = Sms()
    sms.type = "confirmed matches"
    sms.sender = sender
    sms.status = status
    sms.phone = phone
    sms.client_id = client
    sms.message = message
    sms.save()




@login_required
def dashboard(request):
    try:
        current_user = request.user

        client = Client.objects.get(user_id=current_user.id)
        pledges = Pledge.objects.filter(pledge_maker_id=client).aggregate(Count('id'))
        matches = Match.objects.filter(client_id=client).aggregate(Count('id'))
        coins = Coins.objects.filter(client_id=client).aggregate(Sum('amount'))
        context = {'client': client,'pledges':pledges,'matches':matches,'coins':coins}

    except Client.DoesNotExist:
        raise Http404("Client does not exist")
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
            messages.success(request, 'Profile update successful')

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

        coins = Coins.objects.filter(client_id=client).aggregate(Sum('amount')).get('amount__sum', 0.00)

        try:
            if coins  >= 100.00:
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

                Coins.objects.filter(client_id=client).update(amount=F('amount')-100)

                messages.success(request, 'Pledge created successfully')
            else:

                messages.warning(request, "Please top up your coins in order to pledge. Your coins balance is too low. Balance is " + str(coins))


            return redirect('pledges')
        except:

            messages.warning(request,
                             "Please purchase coins in order to pledge ")

            return redirect('pledges')


    else:

        return render(request, 'pledges/make.html')

@login_required
def pledges(request):
    page = request.GET.get('page', 1)
    current_user = request.user
    try:
        client = Client.objects.get(user_id=current_user.id)
        data=Pledge.objects.filter(Q(pledge_maker_id=client) | Q(pledge_maker_id=client)).order_by('-id').all()
        paginator = Paginator(data, 50)


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

    current_user = request.user
    client = Client.objects.get(user_id=current_user.id)


    Coins.objects.filter(client_id=client).update(amount=F('amount') + 100)

    messages.success(request, 'Pledge deleted successfully')

    return redirect('pledges')




def match(request):
    current_user = request.user
    if request.method == "POST":
        try:
            pledger = request.POST.get('pledge')
            amount = request.POST.get('amount')
            receiver = request.POST.get('client')

            client = Client.objects.get(id=receiver)

            pledge_details = Pledge.objects.get(id=pledger)


            #receiverName =client.mobile_money_name;

            #receiverPhone =client.mobile_money_phone;
            #receiverID =client.user_id;

            # insert into match table
            match=Match()
            match.pledge_id= pledge_details
            match.amount=amount
            match.confirmed=0
            match.client_id=client
            match.type="receive"
            match.sms=0
            match.save()
            #print(pledge_details)

            messages.success(request, 'Match created')

            return redirect('match')


        except:
            #print('gad error')
            messages.error(request, 'Error creating match')
            return redirect('match')


    else:
        clients = Client.objects.all()
        pledges = Pledge.objects.filter(payment_confirm='Unconfirmed').order_by('-id').all()
        context = {'clients': clients,'pledges':pledges}

        return render(request, 'matches/make.html',context)

@login_required
def matches(request):
    page = request.GET.get('page', 1)
    current_user = request.user
    if request.user.is_superuser:
        data=Match.objects.all()
    else:


        client = Client.objects.get(user_id=current_user.id)

        data = Match.objects.filter(client_id=client).all()
    paginator = Paginator(data, 50)

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    return render(request, 'matches/index.html', {'data': records})

def delete_match(request, object_id):
    object = get_object_or_404(Match, pk=object_id)
    object.delete()
    messages.success(request, 'Match deleted successfully')

    return redirect('matches')


def matche_confirmed(request, object_id):
    current_user = request.user

    client = Client.objects.get(user_id=current_user.id)

    data = Match.objects.filter(id=object_id).get()
    #print(data.pledge_id.id)

    Pledge.objects.filter(id=data.pledge_id.id).update(payment_confirm='confirmed')

    Match.objects.filter(id=object_id).update(confirmed='confirmed',sms=1)

    # send sms to matches
    pledgerData=Pledge.objects.filter(id=data.pledge_id.id).get()

    #print( pledgerData.pledge_maker_id.mobile_money_name)

    name = pledgerData.pledge_maker_id.mobile_money_name;
    phone =pledgerData.pledge_maker_id.mobile_money_phone;
    message = "Hi " + name + " your payment of  GHS"+str(data.amount)+ " to " + client.firstname+ " has been confirmed successfully" \
                                                                                                  "" \
                                                                                                  ".Your return is between 1-15days";


    send_sms(phone, message,current_user.id)

    messages.success(request, 'payment confirmed successfully')


    return redirect('matches')

def sendMatchNotification(request):
    current_user = request.user
    data = Match.objects.filter(sms=0).all()



    for q in data:
        name = q.client_id.mobile_money_name;
        phone = q.client_id.mobile_money_phone;
      #  d_date = datetime.datetime.strptime(q.pledge_id.payment_deadline, '%Y-%m-%d %H:%M:%S.%f')
        mature=format(q.pledge_id.payment_deadline.strftime('%A, %d %B %Y at %H:%M'))
        message = "Hi " + name + " You have been matched to fulfil your pledge of GHS" + str(
            q.amount) + " to " + q.client_id.firstname + " on payitgh.com.Deadline for payment is " + str(mature) + "check your dashboard for details"
        send_sms(phone, message, current_user.id)

        Match.objects.update(sms=1)


    messages.success(request, 'sms notifications send successfully')

    return redirect('matches')




