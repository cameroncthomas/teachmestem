from django.core.mail import send_mail
from django.shortcuts import redirect, render


from .forms import CourseRegisterForm
from .models import Course


def courses(request):
    """Show courses page."""
    courses = Course.objects.select_related(
        "instructor",
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
    ).order_by("date", "examboard__subject__name")
    context = {
        "courses": courses,
    }
    return render(request, "courses/courses.html", context)


def courses_register(request, course_id):
    """Show course registration page."""
    course = Course.objects.select_related(
        "examboard",
        "examboard__subject",
        "examboard__subject__qualification",
        "instructor",
    ).get(id=course_id)
    if request.method != "POST":
        form = CourseRegisterForm()
    else:
        form = CourseRegisterForm(data=request.POST)
        if form.is_valid():
            send_mail(
                subject=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} has registered interest in a course!",
                message=f"""Requested course: {course.examboard.subject.qualification} {course.examboard.subject} {course.examboard}
                    Course date: {course.date}
                    Course instructor: {course.instructor}
                    Course price: £{course.price}
                    Name: {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]} 
                    Email: {form.cleaned_data["email"]}
                    """,
                from_email=None,
                recipient_list=[],
            )
            form.save()
            return redirect("courses:courses_register_success", course_id)

    context = {
        "course": course,
        "form": form,
    }
    return render(request, "courses/courses_register.html", context)


def courses_register_success(request, course_id):
    """Show course registration form success page."""
    return render(request, "courses/courses_register_success.html")
