import datetime
from django.db import models
from django.utils import timezone

from .MyConsts import MC


# Create your models here.

class Author(models.Model):
    app_label = 'songsapp'

    name = models.CharField(max_length=MC.MAX_NAME_LENGTH)

    # songs many-to-many
    def __str__(self):
        return self.name


class Song(models.Model):
    app_label = 'songsapp'

    title = models.CharField(max_length=MC.MAX_NAME_LENGTH)
    # realizations one-to-many
    authors = models.ManyToManyField(Author)

    def __str__(self):
        a = self.authors.all()
        a = str(a) if a else "--no-author--"
        return self.title + " (" + a + ")"


class Realization(models.Model):
    app_label = 'songsapp'

    content = models.TextField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    create_date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        a = self.song.authors.all()
        a = str(a) if a else "--no-author--"
        return self.song.title + " -- |" + a + "| -- " + " (" + self.content[:50] + "...)"

    def was_created_recently(self):
        return timezone.now() >= self.create_date >= timezone.now() - datetime.timedelta(days=1)


def start_fill():
    pass
