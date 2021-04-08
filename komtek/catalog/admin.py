from django.contrib import admin
from .models import Handbook, Element, HandbookVersion


@admin.register(Handbook)
class HandbookAdmin(admin.ModelAdmin):
    """Administration object for Handbook models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('title', 'short_title', 'version', 'date')
    list_filter = ('date', )


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    """Administration object for Element models.
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('code', 'value', 'handbook', 'version')


@admin.register(HandbookVersion)
class HandbookVersionAdmin(admin.ModelAdmin):
    """Administration object for HandbookVersion models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
    """
    list_display = ('handbook', 'version', 'date')
    list_filter = ('version',)


# admin.site.register(Handbook, HandbookAdmin)
# admin.site.register(Element, ElementAdmin)

