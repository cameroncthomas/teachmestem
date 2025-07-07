from django.contrib import admin

from .models import Course, CourseRegisterUser


class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
        "instructor",
        "date",
        "price",
    ]


class CourseRegisterUserAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "course__instructor",
        "first_name",
        "last_name",
        "email",
    ]


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseRegisterUser, CourseRegisterUserAdmin)
