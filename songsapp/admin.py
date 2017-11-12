from django.contrib import admin

from .models import Author, Song, Realization, Tag, HierarchyItem

# Register your models here.

# class SongAdmin(admin.ModelAdmin):
#     model = Song
#     list_display = ['title', 'get_name', ]
#
#     def get_name(self, obj):
#         return obj.realization_set.all()
#
#     get_name.admin_order_field = 'id'  # Allows column order sorting
#     get_name.short_description = 'Author Name'  # Renames column head
#
#     # Filtering on side - for some reason, this works
#     # list_filter = ['title', 'author__name']


# admin.site.register(Book, BookAdmin)

admin.site.register(Author, Song, Realization, Tag, HierarchyItem)
