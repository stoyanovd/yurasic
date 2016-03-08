from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from django.utils import timezone
# from django.template import loader
from .models import Song, Author, Realization


# Create your views here.
class SongsIndexView(generic.ListView):
    template_name = 'songsapp/index.html'
    context_object_name = 'alphabet_songs_list'

    def get_queryset(self):
        return Song.objects.order_by('title')
        # def get_queryset(self):
        #     """Return 20 first in alphabet songs"""
        #     return Song.objects.order_by('title')[:20]


class AuthorsIndexView(generic.ListView):
    template_name = 'songsapp/authors_index.html'
    context_object_name = 'authors_dict'

    def get_queryset(self):
        return Author.objects.order_by('title')


class DetailView(generic.DetailView):
    model = Song
    template_name = 'songsapp/detail.html'


class ContentView(generic.DetailView):
    model = Song
    template_name = 'songsapp/song_realizations.html'
    # context_object_name = 'rr'
    #
    # def get_queryset(self):
    #     return self


#
# def index(request):
#     alphabet_songs_list = Song.objects.order_by('title')[:5]
#     # template = loader.get_template('songsapp/index.html')
#     context = {
#         'alphabet_songs_list': alphabet_songs_list
#     }
#     return render(request, 'songsapp/index.html', context)
#     # template.render(context, request))
#
#
# def detail(request, song_id):
#     song = get_object_or_404(Song, pk=song_id)
#     return render(request, 'songsapp/detail.html', {'song': song})
#
#
# def content(request, song_id):
#     response = "You are looking at content of song with id %s."
#     return HttpResponse(response % song_id)
#

def add_some(request, song_id):
    return HttpResponse("You want to add sth to song with id %s." % song_id)
