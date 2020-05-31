from django.urls import re_path,path
from django.contrib.auth import views as auth_views
from . import views, forms
urlpatterns = [
    path('', views.empty_view, name='empty'),

    re_path(r'^login/$', views.login_view, name='login'),

    re_path(r'^logout/$', views.logout_view, name='logout'),

    re_path(r'^make_recognition/$', views.make_recognition, name='make_recognition'),

    re_path(r'^train/$', views.extract_and_train, name='extract_and_train'),

    re_path(r'^record/$', views.record, name='record'),

    re_path(r'^rec$', views.rec, name='rec'),

    re_path(r'^save/$', views.save, name='save'),

    re_path(r'^attendance/$', views.attendance, name='attendance'),

    re_path(r'^statistic/$', views.statistic, name='statistic'),

    re_path(r'^statistic/(?P<id>[0-9-]{1,13})/$', views.stat2, name='stat2'),

    re_path(r'^profile/', views.profile, name='profile')


]
