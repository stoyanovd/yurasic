from django.contrib import admin

from .models import Author, Song, Realization, Tag, HierarchyItem

# Register your models here.

admin.site.register([Author, Song, Realization, Tag, HierarchyItem])
