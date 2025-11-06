from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm


def index(request):
    """Home page for revision app."""
    return render(request, "home/index.html")


def privacy(request):
    """Show privacy page."""
    return render(request, "home/privacy.html")


def terms(request):
    """Show terms page."""
    return render(request, "home/terms.html")


def contact(request):
    """Show contact page."""

    if request.method != "POST":
        form = ContactForm()
    else:
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                subject=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} has sent a contact request",
                message=f"""
                    Name: {form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}
                    Email: {form.cleaned_data["email"]}
                    Message:
                    
                    {form.cleaned_data["text"]}
                    
                    """,
                from_email=None,
                recipient_list=[],
            )
            return redirect("home:contact_sent")

    context = {
        "form": form,
    }
    return render(request, "home/contact.html", context)


def contact_sent(request):
    """Show contact form success page."""
    return render(request, "home/contact_sent.html")


@login_required
def my_account(request):
    """Show available options relating to account for logged in users."""
    return render(request, "home/my_account.html")


def pricing(request):
    """Show pricing page."""
    return render(request, "home/pricing.html")
