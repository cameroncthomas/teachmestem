from django.core.mail import send_mail
from django.shortcuts import render

from revision.models import Qualification

from .forms import TutoringContactForm


def tutoring(request):
    """Show tutoring page."""
    is_request_htmx = request.headers.get("HX-Request") == "true"
    qualifications = Qualification.objects.order_by("qualification_number")
    context = {
        "is_request_htmx": is_request_htmx,
        "qualifications": qualifications,
    }
    return render(request, "tutoring/tutoring.html", context)


def tutoring_contact(request):
    """Show tutoring contact page."""
    qualifications = Qualification.objects.order_by("qualification_number")

    if request.method != "POST":
        form = TutoringContactForm()
    else:
        form = TutoringContactForm(data=request.POST)
        if form.is_valid():
            send_mail(
                subject=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} has requested tutoring!",
                message=f"""Requested tutor: {form.cleaned_data['tutor_name']}
                    Name: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']} 
                    Email: {form.cleaned_data['email']}
                    Message:
                    
                    {form.cleaned_data['message']}
                    
                    """,
                from_email=None,
                recipient_list=[],
            )
            form.save()
            context = {
                "qualifications": qualifications,
                "form": form,
            }
            return render(request, "tutoring/tutoring_contact_sent.html", context)

    context = {
        "qualifications": qualifications,
        "form": form,
    }
    return render(request, "tutoring/tutoring_contact.html", context)
