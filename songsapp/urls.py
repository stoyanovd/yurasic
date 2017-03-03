from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'songsapp'

urlpatterns = [
    url(r'^songs/$', views.SongsIndexView.as_view(), name='index'),
    url(r'^authors/$', views.AuthorsIndexView.as_view(), name='authors_index'),
    url(r'^authors/(?P<author_id>[0-9]+)/$', views.one_author_index, name='one_author_index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^songs/(?P<pk>[0-9]+)/$', views.ContentView.as_view(), name='detail'),
    url(r'^songs/(?P<pk>[0-9]+)/song_realizations/$', views.ContentView.as_view(), name='song_realizations'),
    url(r'^songs/(?P<song_id>[0-9]+)/add_some/$', views.add_some, name='add_some'),

    # sth outdated
    # url(r'^mongo_import/$', views.mongo_import, name='mongo_import'),

    url(r'^import_from_old/$', views.import_from_old, name='import_from_old'),
]

urlpatterns += staticfiles_urlpatterns()
