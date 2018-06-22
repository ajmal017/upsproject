from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views

app_name = 'website'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.homeView, name='home'),
    url(r'profileview/$', views.profileview, name='profileview'),
    url(r'profilesaveview/$', views.profilesaveview, name='profilesaveview'),
    url(r'scriptview/$', views.scriptview, name='scriptview'),
    url(r'scriptview/list/$', views.scriptListView, name='scriptListView'),
    url(r'scriptview/(?P<pk>\d+)/edit/$', views.scripteditview, name='scripteditview'),
    url(r'scripteditedview/$', views.scripteditedview, name='scripteditedview'),
    url(r'strategyview/(?P<pk>\d+)/edit/$', views.strategyeditview, name='strategyeditview'),
    url(r'strategyview/(?P<pk>\d+)/del/$', views.strategydelview, name='strategydelview'),
    url(r'strategyview/$', views.strategyview, name='startegyview'),
    url(r'strategyListView/$', views.strategyListView, name='strategyListView'),
    url(r'strategyaddview/$', views.strategyaddview, name='strategyaddview'),
    url(r'tradingview/$', views.tradingview, name='tradingview'),
    url(r'tradingview/list/$', views.tradingListView, name='tradingListView'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
]
