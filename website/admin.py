from django.contrib import admin
from .models import Title

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['show_id', 'title', 'type', 'release_year', 'rating', 'date_added']
    list_filter = ['type', 'rating', 'release_year']
    search_fields = ['title', 'director', 'cast', 'description']
    ordering = ['title']
    readonly_fields = ['show_id']  # Prevent editing show_id after creation
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('show_id', 'type', 'title', 'release_year', 'rating')
        }),
        ('Content Details', {
            'fields': ('director', 'cast', 'duration', 'description')
        }),
        ('Metadata', {
            'fields': ('country', 'date_added', 'listed_in')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()
