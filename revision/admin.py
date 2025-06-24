from django.contrib import admin

from .models import (
    ContactUser,
    ExamBoard,
    ExamBoardCompletion,
    PastPaper,
    PastPaperCompletion,
    Qualification,
    Subject,
    Topic,
    TopicCompletion,
    UserExamBoard,
)


class ContactUserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]


class QualificationAdmin(admin.ModelAdmin):
    list_display = ["__str__", "qualification_number"]


class SubjectAdmin(admin.ModelAdmin):
    list_display = ["__str__", "qualification", "subject_number"]


class ExamboardAdmin(admin.ModelAdmin):
    list_display = ["__str__", "subject", "subject__qualification"]


class PastPaperAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
    ]


class TopicAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
    ]


class TopicCompletionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "topic",
        "topic__examboard",
        "topic__examboard__subject",
        "topic__examboard__subject__qualification",
        "is_complete",
    ]


class PastPaperCompletionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "pastpaper",
        "pastpaper__examboard",
        "pastpaper__examboard__subject",
        "pastpaper__examboard__subject__qualification",
        "is_complete",
    ]


class ExamBoardCompletionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
    ]


class UserExamBoardAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
    ]


admin.site.register(ContactUser, ContactUserAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ExamBoard, ExamboardAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(PastPaper, PastPaperAdmin)
admin.site.register(TopicCompletion, TopicCompletionAdmin)
admin.site.register(PastPaperCompletion, PastPaperCompletionAdmin)
admin.site.register(ExamBoardCompletion, ExamBoardCompletionAdmin)
admin.site.register(UserExamBoard, UserExamBoardAdmin)
