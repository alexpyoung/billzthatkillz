from django.contrib import admin

from lib.admin import link

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    def vendor_link(self, purchase):
        return link(
            f"/admin/vendors/vendor/{purchase.vendor.id}", purchase.vendor.name
        )

    fields = ("id", "date", "vendor_link", "amount", "currency")
    readonly_fields = ("id", "date", "vendor_link", "amount", "currency")
    date_hierarchy = "date"
    list_display = ("id", "date", "vendor_link", "amount", "currency")
    list_filter = ("date", "currency")
    search_fields = ["vendor__name"]
