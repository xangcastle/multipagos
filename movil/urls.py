from django.conf.urls import *

from movil import views

urlpatterns = patterns('',
   url(r'^login/$', views.LoginView.as_view()),
   url(r'^logout/$', views.LogoutView.as_view()),
   url(r'^register/$', views.RegisterView.as_view()),
   url(r'^get_user/$', 'movil.views.get_user', name='get_user'),
   url(r'^get_paquetes/$', 'movil.views.get_paquetes', name='get_paquetes'),
   url(r'^get_paquete/$', 'movil.views.get_paquete', name='get_paquete'),
   url(r'^$', views.TestPageView.as_view()),
)

