import time

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Song, Author, Realization


# Create your views here.
class AllSongsIndexView(generic.ListView):
    template_name = 'songsapp/all_songs_index.html'
    context_object_name = 'alphabet_songs_list'

    def get_queryset(self):
        return Song.objects.order_by('title')


class AuthorsIndexView(generic.ListView):
    template_name = 'songsapp/hierarchy_list.html'
    context_object_name = 'authors_list'

    def get_queryset(self):
        return Author.objects.order_by('name')


def one_author_index(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    one_author_list = author.song_set.order_by('title')
    context = {'author': author, 'one_author_list': one_author_list}
    return render(request, 'songsapp/one_author_list.html', context)


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


# Create your views here.
class HierarchyView(generic.DetailView):
    template_name = 'songsapp/index.html'
    context_object_name = 'nodes_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HierarchyView, self).get_context_data(**kwargs)
        # Add in the publisher

        if hasattr(self.object, 'author'):
            name = self.object.author.name
        elif hasattr(self.object, 'song'):
        context['node'] = self.publisher
        return context

    def get_queryset(self):
        return self.object.children.order_by('id')
        # def get_queryset(self):
        #     """Return 20 first in alphabet songs"""
        #     return Song.objects.order_by('title')[:20]

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

# def add_some(request, song_id):
#     return HttpResponse("You want to add sth to song with id %s." % song_id)
