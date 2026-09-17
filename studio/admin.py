from django.contrib import admin
from django.utils.html import format_html

from .models import Drawing, Enquiry


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "style", "is_featured", "position")
    list_editable = ("is_featured", "position")
    list_filter = ("style", "is_featured")
    search_fields = ("title", "caption")
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(description="Page")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:56px;border:1px solid #ddd" />', obj.image.url
            )
        return "—"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "interest", "email", "phone", "created", "replied")
    list_filter = ("interest", "replied", "created")
    search_fields = ("name", "email", "phone", "message")
    list_editable = ("replied",)
    readonly_fields = ("name", "email", "phone", "interest", "message", "created")


admin.site.site_header = "Dreamy Roses"
admin.site.site_title = "Dreamy Roses"
admin.site.index_title = "Shop admin"
