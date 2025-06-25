from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
        "instructor",
        "date",
        "price",
    ]


admin.site.register(Course, CourseAdmin)
