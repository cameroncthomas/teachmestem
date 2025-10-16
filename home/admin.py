from django.contrib import admin

from .models import ContactUser


class ContactUserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]


admin.site.register(ContactUser, ContactUserAdmin)
