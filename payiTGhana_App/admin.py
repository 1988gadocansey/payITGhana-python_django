from django.contrib import admin
from .models import Client
from .models import Pledge
from .models import Match


admin.site.site_header = 'PayiT Ghana - Administration'

#admin.site.register(Client)
#admin.site.register(Pledge)
#admin.site.register(Match)
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','firstname','lastname','gender','phone','email','mobile_money_phone','mobile_money_name','address','date_joined','user_id','created_at','updated_at']
