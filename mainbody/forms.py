from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import datetime
from .models import check_out, Asset

class check_out_form(forms.ModelForm):
    class Meta:
        model = check_out
        fields = ('assetID','userID','checkdate')
    
    def delete_model(self,request,obj):
        asset_obj = obj.userID
        asset_obj.user = Asset.DEFAULT_USER
        asset_obj.save()
        obj.delete()
        
    def clean(self):
        data = super().clean()# field area specified in class Meta.
        print(data)
        user_name = data.get('userID')
        asset_name = data.get('assetID')
        checkdate = data.get('checkdate')
        # Below are the codes that sync the assigned user to asset information table.
        assetrow = Asset.objects.get(assetname=asset_name) # compared to the method of executing SQL functions in views.py, this method is liter and shorter.
        assetrow.user = str(user_name)
        assetrow.check_out_date = checkdate
        assetrow.save()
        
        # Below are codes that check whether user/item exists.           # Admin should notice that they should input registered user/item only.
        if not User.objects.filter(username = user_name).exists():       # There could be a way for them to choose the user/item rather than inputting
            raise forms.ValidationError('User does not exist.')          # by using assetID/userID as they are foreign keys.
        if not Asset.objects.filter(assetname = asset_name).exists():    # But that would cause problems including database write and namespace conflict.
            raise forms.ValidationError('Asset does not exist.')         # So writing the asset/user would be more convenient.
       
        return data

