from haystack import indexes

from songsapp.models import Tag, Author, Realization, Song


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='name')

    def get_model(self):
        return Tag


class AuthorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='name')

    def get_model(self):
        return Author

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects


class SongIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='title')
    authors = indexes.MultiValueField(model_attr='authors__name')

    def get_model(self):
        return Song

    def prepare_author(self, obj):
        return obj.any_author_name()

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects


class RealizationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    song = indexes.CharField(model_attr='song')
    authors = indexes.MultiValueField(model_attr='song__authors__name')

    def get_model(self):
        return Realization

    # def prepare_author(self, obj):
    #     return self.song.any_author_name()

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects  # .filter(pub_date__lte=datetime.datetime.now())
