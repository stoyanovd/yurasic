from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from . import views

app_name = 'songsapp'

urlpatterns = [
    url(r'^all_songs/$', views.AllSongsIndexView.as_view(), name='all_songs'),

    url(r'^authors/$', views.AuthorsIndexView.as_view(), name='authors_index'),
    url(r'^authors/(?P<author_id>[0-9]+)/$', views.one_author_index, name='one_author_index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^songs/(?P<pk>[0-9]+)/$', views.ContentView.as_view(), name='song_content'),

    url(r'^catalog/$', RedirectView.as_view(url='catalog/0'), name='hierarchy_root'),
    url(r'^catalog/(?P<pk>[0-9]+)/$', views.HierarchyView.as_view(), name='hierarchy'),

    # url(r'^songs/(?P<pk>[0-9]+)/song_realizations/$', views.ContentView.as_view(), name='song_realizations'),
    # url(r'^songs/(?P<song_id>[0-9]+)/add_some/$', views.add_some, name='add_some'),

    # sth outdated
    # url(r'^mongo_import/$', views.mongo_import, name='mongo_import'),

    # url(r'^import_from_old/$', views.import_from_old, name='import_from_old'),
]

# Search
urlpatterns += [
    url(r'^search/', include('haystack.urls')),
]

urlpatterns += staticfiles_urlpatterns()
