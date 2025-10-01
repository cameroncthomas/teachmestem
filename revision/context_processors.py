from revision.models import Qualification


def qualifications(request):
    qualifications = Qualification.objects.order_by("qualification_number")
    return {"qualifications": qualifications}
