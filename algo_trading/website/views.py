# Create your views here.
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.exceptions import *
from _ast import *
from django.db.models.sql.where import OR
from .models import *
from .forms import *
from init_python import *
import json
from utils import *
from pprint import pprint

@validation(login_validator, if_invalid='ADMIN')
def scriptview(request):
    if request.method == 'POST' :
        form = ScriptForm(request.POST)
        context = {"scriptList":getScripts, "form":form,"scriptList":getScripts, "scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}

    else:
        form = ScriptForm()
        context = {"scriptList":getScripts, "form":form,  "timeFrames":getTimeFrmaes, "scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'scripts.html', context)

@validation(login_validator, if_invalid='ADMIN')
def scriptListView(request):
    if request.method == 'POST' :
        form = ScriptForm(request.POST)
        if form.is_valid() :
            st_id = request.POST.get('selStrategyName')
            tr_id = form.cleaned_data['selTradeType']
            sc_id = form.cleaned_data['selScriptName']
            hid_sc_id = request.POST.get('hid_script_id', None)
            operation = request.POST.get('operation', None)
            print(hid_sc_id, operation)
            if operation != None and operation == "del":
                print ("Del ops")
                deleteScript(hid_sc_id)
            elif operation != None and operation == "edit":
                print ("Eidt ops")
                sc = getScript(hid_sc_id)
                form = AddScriptForm(instance=sc)
                context = {"form":form, "scripts": getScripts,  "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
                return render(request, 'scriptEdit.html', context)
            else :
                errorMsg = saveScripts(st_id, tr_id, sc_id)
                stList = getScripts()
                context = {"is_error":True,'errorMsg':errorMsg,"form":form,"scripts": getScripts, "scriptList":stList, "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}

        else:
            form = ScriptForm()
            context = {"form":form, "scripts": getScripts,  "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
        return render(request, 'scripts.html', context)

@validation(login_validator, if_invalid='ADMIN')
def scripteditview(request, pk):
    print("edit view")
    if request.method == 'POST' :
        print("in POST")
        form = AddScriptForm(request.POST)
        if form.is_valid() :
            pk = form.cleaned_data['st_id']
            script_modal = form.save(commit=False)
            script_modal.script_id = pk
            script_modal.save()
        return redirect('/algotrade/scriptview/',request)
    else:
        sc_modal = getScript(pk)
        print(sc_modal.script_id)
        form = AddScriptForm()
        form.fields['st_id'].initial = pk
        form.fields['script_name'].initial = sc_modal.script_name
        form.fields['selTradeType'].initial = sc_modal.trade.trade_id
        form.fields['selStrategyName'].initial = sc_modal.strategy.strategy_id
        form.fields['exchange_type'].initial = sc_modal.exchange_type
        form.fields['is_strategy_active'].initial = sc_modal.is_strategy_active
        print(sc_modal.is_strategy_active)
        context = {"form":form, "scripts": getScripts,  "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'scriptEdit.html', context)

@validation(login_validator, if_invalid='ADMIN')
def strategyview(request):
    print("view")
    if request.method == 'POST' :
        print("POST")
        form = StrategyForm(request.POST)
        context = {"form":form, "stList":getStrategies,"timeFrames":getTimeFrmaes,"scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    else:
        print("normal")
        form = StrategyForm()
        context = {"form":form, "stList":getStrategies,"timeFrames":getTimeFrmaes, "scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'strategy.html', context)

@validation(login_validator, if_invalid='ADMIN')
def scripteditedview(request):
    print("edited view")
    if request.method == 'POST' :
        print("in POST")
        ops = request.POST.get("ops")
        form = AddScriptForm(request.POST)
        if form.is_valid() :
            sc_id = request.POST.get("st_id")
            st_id = request.POST.get('selStrategyName')
            tr_id = request.POST.get('selTradeType')
            sc_name=request.POST.get('script_name')
            ex_type=request.POST.get('exchange_type')
            is_active= form.cleaned_data['is_strategy_active']
            script_modal = getScript(sc_id)
            if(ops == 'Edit'):
                script_modal.script_name = sc_name
                script_modal.exchange_type = ex_type
                script_modal.is_strategy_active = is_active
                print(is_active)
                script_modal.strategy = Strategy.objects.get(strategy_id=st_id)
                script_modal.trade = Trade.objects.get(trade_id=tr_id)
                script_modal.save()
            else :
                script_modal.delete()
        return redirect('/algotrade/scriptview/',request)
    else:
        sc_modal = getScript(pk)
        form = AddScriptForm(instance=sc_modal)
        form.fields['st_id'].initial = pk
        context = {"form":form, "scripts": getScripts,  "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'scriptEdit.html', context)

@validation(login_validator, if_invalid='ADMIN')
def strategyaddview(request):
    print("add view")
    if request.method == 'POST' :
        print("in POST")
        form = AddStrategyForm(request.POST)
        if form.is_valid() :
            ops= form.cleaned_data['ops']
            st_id = form.cleaned_data['st_id']
            if ops == 'Add':
                strategy_modal = form.save()
            elif ops== 'Edit' :

                strategy_modal = form.save(commit=False)
                strategy_modal.strategy_id = st_id
                strategy_modal.save()
            elif ops == 'Del':
                strategy_modal = getStrategy(st_id)
                strategy_modal.delete()
            return redirect('/algotrade/strategyview/',request)
    else:
        form = AddStrategyForm()
        context = {"form":form, "timeFrames":getTimeFrmaes, "targets": getTargets, "stoploss":getStoploss, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'strategyAdd.html', context)

@validation(login_validator, if_invalid='ADMIN')
def strategyeditview(request, pk):
    print("edit view")
    if request.method == 'POST' :
        print("in POST")
        form = AddStrategyForm(request.POST)
        if form.is_valid() :
            strategy_modal = form.update()
            return redirect('/algotrade/strategyview/',request)
    else:
        st= getStrategy(pk)
        print(st.strategy_id)
        form = AddStrategyForm(instance=st)
        form.fields['st_id'].initial = st.strategy_id

        context = {"form":form, "editOps":True,"timeFrames":getTimeFrmaes, "targets": getTargets, "stoploss":getStoploss, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'strategyAdd.html', context)

@validation(login_validator, if_invalid='ADMIN')
def strategydelview(request, pk):
    print("del view")
    if request.method == 'POST' :
        print("in POST")
        form = AddStrategyForm(request.POST)
        if form.is_valid() :
            strategy_modal = form.update()
            return redirect('/algotrade/strategyview/',request)
    else:
        st= getStrategy(pk)
        print(st.strategy_id)
        st.delete()
    return redirect('/algotrade/strategyview/',request)

@validation(login_validator, if_invalid='ADMIN')
def strategyListView(request):
    if request.method == 'POST' :
        form = StrategyForm(request.POST)
        if form.is_valid() :
            st_id = form.cleaned_data['selStrategyName']
            tf = form.cleaned_data['selTimeFrame']
            stList = getStrategyList(st_id, tf);
        context = {"form":form,"stList":stList,"timeFrames":getTimeFrmaes,"scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    else:
        form = StrategyForm()
        context = {"form":form, "stList":getStrategies,"timeFrames":getTimeFrmaes, "scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'strategy.html', context)

@validation(login_validator, if_invalid='ADMIN')
def tradingview(request):

    if request.method == 'POST' :
        form = TradingForm(request.POST)
        context = {"tradeList":getTrades,"form":form,"scriptList":getScripts, "scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "Anychart Django template",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}

    else:
        form = TradingForm()
        context = {"tradeList":getTrades,"form":form, "timeFrames":getTimeFrmaes, "scripts": getScripts, "startegies":getStrategies, "trades": getTradeTypes, "title": "Anychart Django template",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
    return render(request, 'trading.html', context)

@validation(login_validator, if_invalid='ADMIN')
def tradingListView(request):
    if request.method == 'POST' :
        form = TradingForm(request.POST)
        if form.is_valid() :
            tr_id = form.cleaned_data['selTradeType']
            sc_id = form.cleaned_data['selScriptName']
            hid_sc_id = request.POST.get('hid_script_id', None)
            operation = request.POST.get('operation', None)
            print(hid_sc_id, operation)
            if operation != None and operation == "del":
                print ("Del ops")

            elif operation != None and operation == "edit":
                print ("Eidt ops")
            print(sc_id, tr_id)
            errorMsg = saveTrade(sc_id, tr_id)
            context = {"is_error":True,"errorMsg":errorMsg, "form":form,"scripts": getScripts, "tradeList":getTrades, "startegies":getStrategies, "trades": getTradeTypes, "title": "Anychart Django template",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}

        else:
            form = TradingForm()
            context = {"form":form, "scripts": getScripts, "tradeList":getTrades, "startegies":getStrategies, "trades": getTradeTypes, "title": "Anychart Django template",'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Script of the day'}
        return render(request, 'trading.html', context)

@validation(login_validator, if_invalid='USER')
def profileview(request):
    #print 'Inside profile'
    form = ProfileForm()
    if request.method == 'POST' :
        #print 'POST'
        form = ProfileForm(request.POST)
        form.is_valid()
    #print 'Outside'
    user_id = request.session['userid']
    #print user_id
    user_prof = getUserProfile(user_id)
    #print user_prof
    form.fields['selTradeType'].initial = user_prof.trade_type
    form.fields['selAvailableMargin'].initial = user_prof.available_margin
    #print 'After form Init'
    context = {"trades": getTradeTypes, 'form': form, 'username': request.session['username'], 'is_authenticated': True,'pageTitle':'Profile'}
    #print 'Profile.html'
    return render(request, 'profile.html', context)

def profilesaveview(request):
    #print 'Inside profile'
    form = ProfileForm()
    if request.method == 'POST' :
        #print 'POST'
        form = ProfileForm(request.POST)
        form.is_valid()
    #print 'Outside'
    user_id = request.session['userid']
    #print user_id
    user_prof = getUserProfile(user_id)
    #print user_prof
    #print form.cleaned_data['selAvailableMargin']
    user_prof.trade_type = form.cleaned_data['selTradeType']
    user_prof.available_margin = form.cleaned_data['selAvailableMargin']
    user_prof.save()
    return redirect('/algotrade/profileview', request)

@validation(invalidate_session)
@validation(login_validator)
def homeView(request):
    print 'Firs page for the application. This view should have the @init_form annotation'

def getTradeTypes():
    return Trade.objects.all().order_by('trade_value')

def getTargets():
    return Target.objects.all().order_by('target_desc')

def getStoploss():
    return Stoploss.objects.all().order_by('stoploss_desc')

def getStrategyList(strategy, timef):
    try:
        print(strategy, timef)
        if(strategy != 0 and timef != 0) :
            go  = Strategy.objects.all().filter(strategy_id=strategy, time_frame=timef)
        elif(strategy != 0) :
            print("st")
            go  = Strategy.objects.all().filter(strategy_id = strategy)
        elif(timef != 0) :
            print("tr")
            go  = Strategy.objects.all().filter(time_frame=timef)
        else :
            print("nothing")
            go = getStrategies()
    except ObjectDoesNotExist:
        go = None
    return go

def saveScripts(strategy, timef, scripname):
    try:
        if(scripname != u'0' and strategy != u'0' and timef != u'0') :
            print(scripname, strategy, timef)
            tempscrip = Scripts.objects.get(script_id=scripname)
            scrip = Scripts();
            scrip.script_name = tempscrip.script_name
            scrip.strategy = Strategy.objects.get(strategy_id=strategy)
            scrip.trade = Trade.objects.get(trade_id=timef)
            scrip.save()
            go  = "Successfully saved"
        else :
            go = "All fields are mandatory"
    except ObjectDoesNotExist:
        go = None
    return go

def saveTrade(scripId, tradeId):
    try:
        if(scripId != u'0' and tradeId != u'0') :
            tempscrip = Scripts.objects.get(script_id=scripId)
            trade = Trading();
            trade.script = tempscrip
            trade.trade = Trade.objects.get(trade_id=tradeId)
            trade.save()
            go  = "Successfully saved"
        else :
            go = "All fields are mandatory"
    except ObjectDoesNotExist:
        go = None
    return go

def getScriptList(strategy, timef, scripname):
    try:
        if(scripname != u'0' and strategy != u'0' and timef != u'0') :
            print(scripname, strategy, timef)
            go  = Scripts.objects.all().select_related().filter(script_id=scripname).filter(strategy_id = strategy).filter(trade_id=timef)
        elif(scripname != u'0' and timef != u'0') :
            print("scr", "tr")
            go  = Scripts.objects.all().select_related().filter(script_id=scripname).filter(trade_id=timef)
        elif(scripname != u'0' and strategy != u'0' ) :
            print("scr", "st")
            go  = Scripts.objects.all().select_related().filter(script_id=scripname).filter(strategy_id = strategy)
        elif(strategy != u'0' and timef != u'0') :
            print("st", "tr")
            go  = Scripts.objects.all().select_related().filter(strategy_id = strategy).filter(trade_id=timef)
        elif(scripname != u'0') :
            print("scr")
            go  = Scripts.objects.all().select_related().filter(script_id=scripname)
        elif(strategy != u'0') :
            print("st")
            go  = Scripts.objects.all().select_related().filter(strategy_id = strategy)
        elif(timef != u'0') :
            print("tr")
            go  = Scripts.objects.all().select_related().filter(trade_id=timef)
        else :
            print("nothing")
            go = getScripts()
    except ObjectDoesNotExist:
        go = None
    return go

def getStrategies():
    return Strategy.objects.all().order_by('strategy_name')

def getTrades():
    return Trading.objects.all().order_by('trading_id')

def getScripts():
    return Scripts.objects.all().order_by('script_name')

def getTimeFrmaes():
    return TimeFrame.objects.all().order_by('timeframe_id')
def deleteScript(sc_id):
    scrip = Scripts.objects.get(script_id=sc_id)
    scrip.delete()
def getScript(sc_id):
    try:
        go = Scripts.objects.select_related().get(script_id=sc_id)
    except ObjectDoesNotExist:
        go = None
    return go

def getStrategy(st_id):
    try:
        go = Strategy.objects.get(strategy_id=st_id)
    except ObjectDoesNotExist:
        go = None
    return go

def getTradeList(timef, scripname):
    try:
        if(scripname != u'0' and timef != u'0') :
            print("scr", "tr")
            go  = Scripts.objects.all().select_related().filter(script_id=scripname).filter(trade_id=timef)
        elif(scripname != u'0') :
            print("scr")
            go  = Scripts.objects.all().select_related().filter(script_id=scripname)
        elif(timef != u'0') :
            print("tr")
            go  = Scripts.objects.all().select_related().filter(trade_id=timef)
        else :
            print("nothing")
            go = getScripts()
    except ObjectDoesNotExist:
        go = None
    return go
