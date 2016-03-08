from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'songsapp'

urlpatterns = [
    url(r'^$', views.SongsIndexView.as_view(), name='index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.ContentView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/song_realizations/$', views.ContentView.as_view(), name='song_realizations'),
    url(r'^(?P<song_id>[0-9]+)/add_some/$', views.add_some, name='add_some'),
]

urlpatterns += staticfiles_urlpatterns()
