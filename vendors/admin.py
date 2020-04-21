from django.contrib import admin

from lib.admin import link
from purchases.models import Purchase

from .models import Vendor


class VendorPurchaseAdmin(admin.TabularInline):
    def id_link(self, purchase):
        return link(f"/admin/purchases/purchase/{purchase.id}", purchase.id)

    id_link.short_description = "id"

    model = Purchase
    fk_name = "vendor"
    readonly_fields = (
        "id_link",
        "name",
        "date",
        "vendor",
        "amount",
        "currency",
    )
    can_delete = False


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "name")
    list_display = ("id", "name")
    list_filter = ["name"]
    inlines = [VendorPurchaseAdmin]
