from django.contrib import admin

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "date", "vendor", "amount", "currency")
    date_hierarchy = "date"
    list_display = ("id", "date", "vendor", "amount", "currency")
    list_filter = ("date", "currency")
    search_fields = ["vendor__name"]
