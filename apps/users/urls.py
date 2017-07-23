from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm
urlpatterns = [
    url(r'^register/', views.register, name= 'register'),
    url(r'^profile/', views.profile, name= 'profile'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.set_password, name='set_password'),
    url(r'^', include('django.contrib.auth.urls')),
]
