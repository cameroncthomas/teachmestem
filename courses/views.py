from django.shortcuts import render

from revision.models import Qualification

from .models import Course


def courses(request):
    """Show courses page."""
    qualifications = Qualification.objects.order_by("qualification_number")
    courses = Course.objects.select_related(
        "instructor",
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
    ).order_by("date", "-examboard__subject__name")
    context = {
        "qualifications": qualifications,
        "courses": courses,
    }
    return render(request, "courses/courses.html", context)
