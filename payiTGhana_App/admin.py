from django.contrib import admin
from .models import Client
from .models import Pledge
from .models import Match,Sms,Coins


admin.site.site_header = 'PayiT Ghana - Administration'



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','firstname','lastname','gender','phone','email','mobile_money_phone','mobile_money_name','address','date_joined','user_id','created_at','updated_at']

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ['id','pledge_maker_id','pledge_receiver_id','pledged_amount','maturity_date','payment_confirm','created_at','updated_at']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['id','pledge_id','client_id','amount','type','confirmed','sms','created_at','updated_at']

@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ['id','message','type','status','phone','sender','created_at','updated_at']

@admin.register(Coins)
class CoinsAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['name', 'phone']
    list_display = ['id', 'name', 'phone','amount', 'created_at', 'updated_at']

    list_filter = ('created_at',)

    def name(self, obj):
        return obj.client_id.firstname+" "+obj.client_id.lastname

    def phone(self, obj):
        return "0"+str(obj.client_id.phone)
