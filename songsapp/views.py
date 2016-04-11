import datetime
import time

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


def mongo_import(request):
    print("enter it")
    from pymongo import MongoClient
    client = MongoClient()
    db = client['scrapy']
    collection = db['my_items']
    print(collection)

    counter_in = 0
    counter_success = 0
    start_time = time.time()
    print(collection.count())
    for d in collection.find():
        counter_in += 1
        if not 'author' in d:
            continue
        print(d['author'])
        author = d['author']
        title = d['title']
        url = d['url']
        content = d['content']
        tags = d['tags']

        author_in_ours = Author.objects.filter(name=author)
        print(author_in_ours)
        if len(author_in_ours) > 0:
            our_author = author_in_ours[0]
        else:
            our_author = Author(name=author)
            our_author.save()

        songs_in_ours = Song.objects.filter(authors__in=[our_author], title=title)
        print(songs_in_ours)
        assert len(songs_in_ours) <= 1
        if len(songs_in_ours) == 1:
            our_song = songs_in_ours[0]
        else:
            our_song = Song(title=title)
            our_song.save()
            our_song.authors.add(our_author)

        real_in_ours = Realization.objects.filter(song=our_song, content=content)
        print((real_in_ours))
        if len(real_in_ours) > 0:
            continue
        our_real = Realization(song=our_song, content=content)
        our_real.save()

        counter_success += 1

    end_time = time.time()
    ans_stats = {'counter_in': counter_in,
                 'counter_success': counter_success,
                 'time_processed': end_time - start_time,
                 }
    return HttpResponse(str(ans_stats))


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

#
# class OneAuthorIndexView(generic.ListView):
#     template_name = 'songsapp/one_author_list.html'
#     context_object_name = 'one_author_list'
#
#     def get_queryset(self):
#         return Song.objects.filter().order_by('title')
#

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
