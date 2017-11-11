import datetime
from django.db import models
from django.utils import timezone

from .MyConsts import MC


class Tag(models.Model):
    app_label = 'songsapp'

    # I think we don't need one-letter tags
    # (and not sure that we need two-letters tags)
    # name = models.CharField(max_length=MC.MAX_NAME_LENGTH, blank=False)
    tag = models.SlugField(default="")

    # TODO think about synonyms_namings

    def __str__(self):
        return self.tag


class HierarchyItem(models.Model):
    app_label = 'songsapp'

    parent = models.ForeignKey('self', null=True, related_name='children')
    name = models.CharField(blank=False, max_length=100)

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    #
    def __str__(self):
        return 'HierarchyItem: ' + self.name


class Author(models.Model):
    app_label = 'songsapp'

    name = models.CharField(max_length=MC.MAX_NAME_LENGTH, blank=False)
    tags = models.ManyToManyField(Tag, blank=True)

    node = models.OneToOneField('HierarchyItem', null=True)

    def __str__(self):
        return self.name

        # TODO create_date maybe needed too


class Song(models.Model):
    app_label = 'songsapp'

    title = models.CharField(max_length=MC.MAX_NAME_LENGTH, blank=False)
    # realizations one-to-many
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag, blank=True)

    node = models.OneToOneField('HierarchyItem', null=True, related_name='target')

    def __str__(self):
        return self.title

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
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='realization_set')
    create_date = models.DateTimeField('date created', default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True)

    source_url = models.URLField(blank=True)

    # node = models.OneToOneField('HierarchyItem')

    def was_created_recently(self):
        return timezone.now() >= self.create_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        from django.urls import reverse
        # TODO learn how to use reverse here
        return '/songs/%i/' % self.id

    def __str__(self):  # __unicode__ on Python 2
        return (self.song.title if self.song else "-no-song") + " (real.id:" + str(self.id) + ")"


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TaggedItem(models.Model):
    app_label = 'songsapp'

    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):  # __unicode__ on Python 2
        return self.tag


class Wonder(models.Model):
    app_label = 'songsapp'

    comment = models.TextField(blank=False)
