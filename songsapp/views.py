import time

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Song, Author, Realization, HierarchyItem


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


class SongContentView(generic.DetailView):
    model = Song
    template_name = 'songsapp/song_realizations.html'
    # template_name = 'songsapp/detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super(SongContentView, self).get_context_data(**kwargs)

        cur = self.object.node
        parents = []
        # we will use this for breadcrumb, so minus ourselves:
        cur = cur.parent
        while cur is not None:
            parents += [cur]
            cur = cur.parent
        context['parents'] = reversed(parents)

        return context


class ContentView(generic.DetailView):
    model = Song
    template_name = 'songsapp/song_realizations.html'


    # context_object_name = 'rr'
    #
    # def get_queryset(self):
    #     return self


class HierarchyView(generic.DetailView):
    model = HierarchyItem
    template_name = 'songsapp/index.html'

    context_object_name = 'node'

    def get_context_data(self, **kwargs):
        context = super(HierarchyView, self).get_context_data(**kwargs)

        # children = HierarchyItem.objects.filter(parent_id__exact=self.object.id)
        children = self.object.children.all()
        is_leaf = lambda n: len(n.children.all()) == 0
        song_if_leaf = lambda n: n.song if is_leaf(n) else None

        children = [(n, song_if_leaf(n)) for n in children]
        print(children)
        context['children'] = children

        cur = self.object
        parents = []
        # we will use this for breadcrumb, so minus ourselves:
        cur = cur.parent
        while cur is not None:
            parents += [cur]
            cur = cur.parent
        context['parents'] = reversed(parents)

        return context

        # def get_context_data(self, **kwargs):(self):
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

# def add_some(request, song_id):
#     return HttpResponse("You want to add sth to song with id %s." % song_id)
