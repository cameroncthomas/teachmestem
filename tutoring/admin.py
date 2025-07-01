from django.contrib import admin

from .models import Tutor, TutoringContactUser


class TutorAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "is_available"]


class TutoringContactUserAdmin(admin.ModelAdmin):
    list_display = [
        "tutor",
        "first_name",
        "last_name",
        "email",
    ]


admin.site.register(Tutor, TutorAdmin)
admin.site.register(TutoringContactUser, TutoringContactUserAdmin)
