from django.contrib import admin
from . import models


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    fieldsets = (
        (
            "방 정보",
            {
                "fields": (
                    "manager",
                    "name",
                    "attendee_number",
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "time table",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            },
        ),
    )

    @admin.display(description="방장")
    def manager_name(self, obj):
        return obj.manager.nickname


@admin.register(models.Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    fields = ("room", "user", "is_completed", "created_at", "deleted_at")


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
