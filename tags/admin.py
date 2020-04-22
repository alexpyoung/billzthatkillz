from django.contrib import admin

from lib.admin import link
from vendors.models import Vendor

from .models import Tag


class VendorAdmin(admin.TabularInline):
    def id_link(self, vendor):
        return link(f"/admin/vendors/vendor/{vendor.id}", vendor.id)

    id_link.short_description = "id"

    model = Vendor.tags.through
    list_display = ("id_link", "name")
    can_delete = False


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ["name"]
    inlines = [VendorAdmin]
    search_fields = ["name"]
