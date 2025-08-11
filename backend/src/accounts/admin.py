from django.contrib import admin

from accounts.models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin[UserModel]):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("email", "created_at", "updated_at")
    search_fields = ["email"]
