import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Realization, Song, Author
from django.core.urlresolvers import reverse

# Create your tests here.


class RealizationMethodTests(TestCase):
    def test_song_not_null_constraint(self):
        """ realization can't be saved without song (not-null constraint) """
        from django.db.utils import IntegrityError

        time = timezone.now() + datetime.timedelta(days=30)
        future_realization = Realization(create_date=time)
        self.assertRaises(IntegrityError, future_realization.save)

    def test_was_created_recently_with_future(self):
        """ was_created_recently must return false if future realization s"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_realization = Realization(create_date=time)
        self.assertEqual(future_realization.was_created_recently(), False)

    def test_was_created_recently_within_one_hour(self):
        """ was_created_recently must return false if future realization s"""
        time = timezone.now() - datetime.timedelta(hours=1)
        one_hour_r = Realization(create_date=time)
        self.assertEqual(one_hour_r.was_created_recently(), True)

    def test_was_created_recently_with_old(self):
        """ was_created_recently must return false if future realization s"""
        time = timezone.now() - datetime.timedelta(days=30)
        old_r = Realization(create_date=time)
        self.assertEqual(old_r.was_created_recently(), False)

    def test_index_no_songs(self):
        response = self.client.get(reverse('songsapp:index'))
        self.assertContains(response, 'No songs.', status_code=200)

    def test_index_two_songs(self):
        a = Author.objects.create(name='man1')
        s = Song.objects.create(title='Song1')
        s.authors.add(a)
        s = Song.objects.create(title='Song2')
        s.authors.add(a)

        response = self.client.get(reverse('songsapp:index'))
        self.assertQuerysetEqual(response.context['alphabet_songs_list'],
                                 ['<Song: Song1 ([<Author: man1>])>',
                                  '<Song: Song2 ([<Author: man1>])>'])