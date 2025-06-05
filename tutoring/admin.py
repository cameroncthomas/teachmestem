from django.contrib import admin

from .models import TutoringContactUser


class TutoringContactUserAdmin(admin.ModelAdmin):
    list_display = ["tutor_name", "first_name", "last_name", "email"]


admin.site.register(TutoringContactUser, TutoringContactUserAdmin)
