from django.urls import re_path,path
from django.contrib.auth import views as auth_views
from . import views, forms
urlpatterns = [
    path('', views.empty_view, name='empty'),

    re_path(r'^login/$', views.login_view, name='login'),

    re_path(r'^logout/$', views.logout_view, name='logout'),

    re_path(r'^make_recognition/$', views.make_recognition, name='make_recognition'),

    re_path(r'^extract_and_train/$', views.extract_and_train, name='extract_and_train'),

    re_path(r'^emotion_recognize/$', views.emotion_recognize, name='emotion_recognize')

]
