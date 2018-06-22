from django import forms
from .models import *

class LoginForm(forms.Form):
     username = forms.CharField(max_length=6,required=True)
     password = forms.CharField(required=True)
     birthyear = forms.IntegerField(required=True)

class ProfileForm(forms.Form):
     selAvailableMargin = forms.FloatField(required=True)
     selTradeType = forms.CharField(max_length=1, required=False)

class StrategyForm(forms.Form):
     selStrategyName = forms.IntegerField(required=False)
     selTimeFrame = forms.IntegerField(required=False)

class ScriptForm(forms.Form):
    selTradeType = forms.CharField(max_length=1, required=False)
    selStrategyName = forms.IntegerField(required=False)
    selScriptName = forms.CharField(max_length=20, required=False)

class TradingForm(forms.Form):
    selTradeType = forms.CharField(max_length=1, required=False)
    selScriptName = forms.CharField(max_length=20, required=False)

class AddStrategyForm(forms.ModelForm):
    ops = forms.CharField(max_length=4, required=False)
    st_id = forms.IntegerField(required=False)
    class Meta:
        model = Strategy
        fields = '__all__'

class AddScriptForm(forms.Form):
    ops = forms.CharField(max_length=4, required=False)
    st_id = forms.IntegerField(required=False)
    selTradeType = forms.CharField(max_length=1, required=True)
    selStrategyName = forms.IntegerField(required=True)
    exchange_type = forms.CharField(max_length=10, required=False)
    is_strategy_active = forms.BooleanField(required=False)
    script_name = forms.CharField(max_length=20, required=False)
