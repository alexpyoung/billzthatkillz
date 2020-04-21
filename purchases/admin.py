from django.contrib import admin

from .models import Purchase, Vendor


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "date", "vendor", "amount", "currency")
    date_hierarchy = "date"
    list_display = ("id", "date", "vendor", "amount", "currency")
    list_filter = ("date", "currency")
    search_fields = ["vendor__name"]


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
