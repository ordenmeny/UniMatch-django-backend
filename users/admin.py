from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'chat_id', 'first_name', 'last_name')
    list_display_links = ('username', 'email')
    list_editable = ('chat_id', 'first_name', 'last_name')

    fields_to_set = ("first_name", "last_name", "email", "age", "image", "hobby")
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

class PairsModelAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'user3', 'is_archived')
    list_display_links = ('user1', 'user2', 'user3', 'is_archived')

admin.site.register(PairsModel, PairsModelAdmin)
# admin.site.register(CurrentPairsModel)
