import datetime
from django.db import models
from django.utils import timezone

from .MyConsts import MC


class Tag(models.Model):
    app_label = 'songsapp'

    # I think we don't need one-letter tags
    # (and not sure that we need two-letters tags)
    name = models.CharField(max_length=MC.MAX_NAME_LENGTH, blank=False)
    # TODO think about synonyms


class Author(models.Model):
    app_label = 'songsapp'

    name = models.CharField(max_length=MC.MAX_NAME_LENGTH, blank=False)
    tags = models.ManyToManyField(Tag)

    # TODO create_date maybe needed too


class Song(models.Model):
    app_label = 'songsapp'

    title = models.CharField(max_length=MC.MAX_NAME_LENGTH, blank=False)
    # realizations one-to-many
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag)

    def any_author_name(self):
        a = self.authors.all()
        if a:
            return a.first().name
        else:
            return '#no-author'

            # TODO create_date maybe needed too


class Realization(models.Model):
    app_label = 'songsapp'

    content = models.TextField(blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    create_date = models.DateTimeField('date created', default=timezone.now)
    tags = models.ManyToManyField(Tag)

    source_url = models.URLField(blank=True)

    def was_created_recently(self):
        return timezone.now() >= self.create_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        from django.urls import reverse
        # TODO learn how to use reverse here
        return '/songs/%i/' % self.id


class Wonder(models.Model):
    app_label = 'songsapp'

    comment = models.TextField(blank=False)
