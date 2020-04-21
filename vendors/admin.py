from django.contrib import admin

from purchases.models import Purchase

from .models import Vendor


class VendorPurchaseAdmin(admin.TabularInline):
    model = Purchase
    fk_name = "vendor"
    readonly_fields = ("id", "date", "vendor", "amount", "currency")
    list_display = ("id", "date", "vendor", "amount", "currency")
    can_delete = False


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "name")
    list_display = ("id", "name")
    list_filter = ["name"]
    inlines = [VendorPurchaseAdmin]
