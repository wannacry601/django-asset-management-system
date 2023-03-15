from django.contrib import admin
from mainbody.models import Asset,checkout
from .forms import check_out_form

class check_out_admin(admin.ModelAdmin):
    form = check_out_form


class not_input(admin.ModelAdmin):
    exclude = ('check_out_date',)

    

admin.site.register(Asset,not_input)
admin.site.register(checkout,check_out_admin)