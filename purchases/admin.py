from django.contrib import admin
from django.db.models import DateTimeField, Max, Min, Sum
from django.db.models.functions import Trunc

from lib.admin import link

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    def vendor_link(self, purchase):
        return link(
            f"/admin/vendors/vendor/{purchase.vendor.id}", purchase.vendor.name
        )

    vendor_link.short_description = "vendor"

    change_list_template = "admin/purchase_summary_change_list.html"
    date_hierarchy = "date"
    list_filter = ("date", "currency")
    search_fields = ["vendor__name"]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context,
        )
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            "total": Sum("amount"),
        }
        response.context_data["summary_total"] = dict(qs.aggregate(**metrics))
        response.context_data["summary"] = list(
            qs.values("id", "date", "vendor__id", "vendor__name", "amount")
            .annotate(**metrics)
            .order_by("date")
        )

        summary_over_time = (
            qs.annotate(
                period=Trunc("date", "day", output_field=DateTimeField(),),
            )
            .values("period")
            .annotate(total=Sum("amount"))
            .order_by("period")
        )
        summary_range = summary_over_time.aggregate(
            low=Min("total"), high=Max("total"),
        )
        high = summary_range.get("high", 0)
        low = summary_range.get("low", 0)
        response.context_data["summary_over_time"] = [
            {
                "period": x["period"],
                "total": x["total"] or 0,
                "pct": ((x["total"] or 0) - low) / (high - low) * 100
                if high > low
                else 0,
            }
            for x in summary_over_time
        ]

        return response
