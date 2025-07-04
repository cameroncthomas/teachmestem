from django.core.mail import send_mail
from django.shortcuts import redirect, render

from revision.models import Qualification

from .forms import TutoringContactForm
from .models import Tutor


def tutoring(request):
    """Show tutoring page."""
    qualifications = Qualification.objects.order_by("qualification_number")
    tutors = Tutor.objects.all()
    context = {
        "qualifications": qualifications,
        "tutors": tutors,
    }
    return render(request, "tutoring/tutoring.html", context)


def tutoring_contact(request, tutor_id):
    """Show tutoring contact page."""
    qualifications = Qualification.objects.order_by("qualification_number")
    tutor = Tutor.objects.get(id=tutor_id)
    if request.method != "POST":
        form = TutoringContactForm()
    else:
        form = TutoringContactForm(data=request.POST)
        if form.is_valid():
            send_mail(
                subject=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} has requested tutoring!",
                message=f"""Requested tutor: {tutor.name}
                    Name: {form.cleaned_data['first_name']} {form.cleaned_data['last_name']} 
                    Email: {form.cleaned_data['email']}
                    Message:
                    
                    {form.cleaned_data['message']}
                    
                    """,
                from_email=None,
                recipient_list=[],
            )
            form.save()
            return redirect("tutoring:tutoring_contact_sent", tutor_id)

    context = {
        "qualifications": qualifications,
        "tutor": tutor,
        "form": form,
    }
    return render(request, "tutoring/tutoring_contact.html", context)


def tutoring_contact_sent(request, tutor_id):
    """Show tutoring contact form success page."""
    qualifications = Qualification.objects.order_by("qualification_number")
    context = {"qualifications": qualifications}
    return render(request, "tutoring/tutoring_contact_sent.html", context)
