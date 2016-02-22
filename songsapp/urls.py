from django.conf.urls import url

from . import views

app_name = 'songsapp'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/content/$', views.ContentView.as_view(), name='content'),
    url(r'^(?P<song_id>[0-9]+)/add_some/$', views.add_some, name='add_some'),
]
