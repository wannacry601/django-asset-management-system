from django.contrib import admin
from mainbody.models import Asset,check_out
from .forms import check_out_form

class check_out_admin(admin.ModelAdmin):
    form = check_out_form

class not_input(admin.ModelAdmin):
    exclude = ('check_out_date',)

admin.site.register(Asset,not_input)
admin.site.register(check_out,check_out_admin)