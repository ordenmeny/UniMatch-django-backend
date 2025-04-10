from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'uniq_code', 'chat_id')
    list_display_links = ('username', 'email')
    list_editable = ('uniq_code', 'chat_id')

    fields_to_set = ("first_name", "last_name", "email", "age", "university", "uniq_code", "image", "hobby")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": fields_to_set}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(HobbyModel)

admin.site.register(HistoryPairsModel)
admin.site.register(CurrentPairsModel)
