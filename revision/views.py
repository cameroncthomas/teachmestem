from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.utils.text import slugify

from .forms import ContactForm
from .models import (
    ExamBoard,
    PastPaper,
    PastPaperCompletion,
    Qualification,
    Subject,
    Topic,
    TopicCompletion,
    UserExamBoard,
)


def index(request):
    """Home page for revision app."""
    return render(request, "revision/index.html")


def privacy(request):
    """Show privacy page."""
    return render(request, "revision/privacy.html")


def terms(request):
    """Show terms page."""
    return render(request, "revision/terms.html")


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
            return redirect("revision:contact_sent")

    context = {
        "form": form,
    }
    return render(request, "revision/contact.html", context)


def contact_sent(request):
    """Show contact form success page."""
    return render(request, "revision/contact_sent.html")


@login_required
def qualification(request, qualification_slug):
    """Show all subjects (Subject instances) for a given qualification."""
    qualification = Qualification.objects.get(slug=qualification_slug)
    subjects = Subject.objects.filter(qualification=qualification).order_by(
        "subject_number"
    )
    context = {
        "qualification": qualification,
        "subjects": subjects,
    }
    return render(request, "revision/qualification.html", context)


@login_required
def subject(request, qualification_slug, subject_id, subject_slug):
    """Show all exam boards (ExamBoard instances) for a given subject."""
    subject = Subject.objects.select_related("qualification").get(id=subject_id)
    examboards = ExamBoard.objects.filter(subject=subject)
    context = {
        "subject": subject,
        "examboards": examboards,
    }
    return render(request, "revision/subject.html", context)


@login_required
def examboard(request, qualification_slug, subject_slug, examboard_id, examboard_slug):
    """Show all topics (Topic instances) and past papers (PastPaper instances) for a
    given ExamBoard instance.
    """
    examboard = ExamBoard.objects.select_related(
        "subject", "subject__qualification"
    ).get(id=examboard_id)
    is_examboard_in_my_subjects = UserExamBoard.objects.filter(
        user=request.user, examboard=examboard
    ).exists()
    topics = Topic.objects.filter(examboard=examboard)
    pastpapers = PastPaper.objects.filter(examboard=examboard)
    completed_topics = Topic.objects.filter(
        examboard=examboard,
        topiccompletion__user=request.user,
        topiccompletion__topic__in=topics,
        topiccompletion__is_complete=True,
    )
    completed_pastpapers = PastPaper.objects.filter(
        examboard=examboard,
        pastpapercompletion__user=request.user,
        pastpapercompletion__pastpaper__in=pastpapers,
        pastpapercompletion__is_complete=True,
    )
    num_topics_completed = completed_topics.count()
    num_pastpapers_completed = completed_pastpapers.count()
    total_num_topics = topics.count()
    total_num_pastpapers = pastpapers.count()
    topic_progress_percentage = (
        int(100 * num_topics_completed / total_num_topics)
        if total_num_topics > 0
        else 0
    )
    pastpaper_progress_percentage = (
        int(100 * num_pastpapers_completed / total_num_pastpapers)
        if total_num_pastpapers > 0
        else 0
    )
    context = {
        "examboard": examboard,
        "is_examboard_in_my_subjects": is_examboard_in_my_subjects,
        "topics": topics,
        "pastpapers": pastpapers,
        "completed_topics": completed_topics,
        "completed_pastpapers": completed_pastpapers,
        "num_topics_completed": num_topics_completed,
        "num_pastpapers_completed": num_pastpapers_completed,
        "total_num_topics": total_num_topics,
        "total_num_pastpapers": total_num_pastpapers,
        "topic_progress_percentage": topic_progress_percentage,
        "pastpaper_progress_percentage": pastpaper_progress_percentage,
    }
    if (
        examboard.subject.name == "Maths"
        and examboard.subject.qualification.name == "A Level"
    ):
        context["maths_pure_topics"] = topics.filter(maths_section="pure")
        context["maths_statistics_topics"] = topics.filter(maths_section="statistics")
        context["maths_mechanics_topics"] = topics.filter(maths_section="mechanics")
        return render(request, "revision/examboard_maths.html", context)
    return render(request, "revision/examboard.html", context)


@login_required
def my_subjects(request):
    """Show all exam boards (ExamBoard instances) added to 'My Subjects' by User."""
    my_subjects = UserExamBoard.objects.select_related(
        "examboard", "examboard__subject", "examboard__subject__qualification"
    ).filter(user=request.user)
    context = {
        "my_subjects": my_subjects,
    }
    return render(request, "revision/my_subjects.html", context)


@login_required
def my_account(request):
    """Show available options relating to account for logged in users."""
    return render(request, "revision/my_account.html")


@login_required
def add_examboard_to_my_subjects(request, examboard_id):
    """Add ExamBoard to 'My Subjects' (create UserExamBoard instance)."""
    if request.method != "POST":
        raise Http404
    if UserExamBoard.objects.filter(
        user=request.user, examboard__id=examboard_id
    ).exists():
        raise Http404
    is_examboard_in_my_subjects = True
    examboard = ExamBoard.objects.get(id=examboard_id)
    UserExamBoard.objects.create(user=request.user, examboard=examboard)
    context = {
        "is_examboard_in_my_subjects": is_examboard_in_my_subjects,
        "examboard": examboard,
    }
    return render(request, "revision/snippets/my_subjects_btns.html", context)


@login_required
def remove_examboard_from_my_subjects(request, examboard_id):
    """Remove ExamBoard from 'My Subjects' (delete UserExamBoard instance)."""
    if request.method != "POST":
        raise Http404
    if not UserExamBoard.objects.filter(
        user=request.user, examboard__id=examboard_id
    ).exists():
        raise Http404
    is_examboard_in_my_subjects = False
    examboard = ExamBoard.objects.get(id=examboard_id)
    my_subject = UserExamBoard.objects.get(user=request.user, examboard=examboard)
    my_subject.delete()
    context = {
        "is_examboard_in_my_subjects": is_examboard_in_my_subjects,
        "examboard": examboard,
    }
    return render(request, "revision/snippets/my_subjects_btns.html", context)


@login_required
def mark_topic_as_complete(request, topic_id):
    """Update Topic as complete for User (update or create TopicCompletion instance)."""
    if request.method != "POST":
        raise Http404
    if TopicCompletion.objects.filter(
        user=request.user, topic__id=topic_id, is_complete=True
    ).exists():
        raise Http404
    is_request_htmx = request.headers.get("HX-Request") == "true"
    topic = Topic.objects.select_related(
        "examboard", "examboard__subject", "examboard__subject__qualification"
    ).get(id=topic_id)
    examboard = topic.examboard
    topic_completion = TopicCompletion.objects.get_or_create(
        user=request.user, topic=topic, is_complete=False
    )[0]
    topic_completion.is_complete = True
    topic_completion.save()
    num_topics_completed = TopicCompletion.objects.filter(
        user=request.user, topic__examboard=topic.examboard, is_complete=True
    ).count()
    total_num_topics = Topic.objects.filter(examboard=topic.examboard).count()
    topic_progress_percentage = (
        int(100 * num_topics_completed / total_num_topics)
        if total_num_topics > 0
        else 0
    )
    context = {
        "is_request_htmx": is_request_htmx,
        "topic": topic,
        "examboard": examboard,
        "num_topics_completed": num_topics_completed,
        "total_num_topics": total_num_topics,
        "topic_progress_percentage": topic_progress_percentage,
    }
    return render(request, "revision/snippets/complete_topic_card.html", context)


@login_required
def mark_topic_as_uncomplete(request, topic_id):
    """Update Topic as uncomplete for User (update TopicCompletion instance)."""
    if request.method != "POST":
        raise Http404
    if (
        not TopicCompletion.objects.filter(
            user=request.user, topic__id=topic_id, is_complete=True
        ).exists()
        or TopicCompletion.objects.filter(
            user=request.user, topic__id=topic_id, is_complete=False
        ).exists()
    ):
        raise Http404
    is_request_htmx = request.headers.get("HX-Request") == "true"
    topic = Topic.objects.select_related(
        "examboard", "examboard__subject", "examboard__subject__qualification"
    ).get(id=topic_id)
    examboard = topic.examboard
    topic_completion = TopicCompletion.objects.get(
        user=request.user, topic=topic, is_complete=True
    )
    topic_completion.is_complete = False
    topic_completion.save()
    num_topics_completed = TopicCompletion.objects.filter(
        user=request.user, topic__examboard=topic.examboard, is_complete=True
    ).count()
    total_num_topics = Topic.objects.filter(examboard=topic.examboard).count()
    topic_progress_percentage = (
        int(100 * num_topics_completed / total_num_topics)
        if total_num_topics > 0
        else 0
    )
    context = {
        "is_request_htmx": is_request_htmx,
        "topic": topic,
        "examboard": examboard,
        "num_topics_completed": num_topics_completed,
        "total_num_topics": total_num_topics,
        "topic_progress_percentage": topic_progress_percentage,
    }
    return render(request, "revision/snippets/uncomplete_topic_card.html", context)


@login_required
def mark_pastpaper_as_complete(request, pastpaper_id):
    """Update PastPaper as complete for User (update or create PastPaperCompletion instance)."""
    if request.method != "POST":
        raise Http404
    if PastPaperCompletion.objects.filter(
        user=request.user, pastpaper__id=pastpaper_id, is_complete=True
    ).exists():
        raise Http404
    is_request_htmx = request.headers.get("HX-Request") == "true"
    pastpaper = PastPaper.objects.select_related(
        "examboard", "examboard__subject", "examboard__subject__qualification"
    ).get(id=pastpaper_id)
    examboard = pastpaper.examboard
    pastpaper_completion = PastPaperCompletion.objects.get_or_create(
        user=request.user, pastpaper=pastpaper, is_complete=False
    )[0]
    pastpaper_completion.is_complete = True
    pastpaper_completion.save()
    num_pastpapers_completed = PastPaperCompletion.objects.filter(
        user=request.user, pastpaper__examboard=pastpaper.examboard, is_complete=True
    ).count()
    total_num_pastpapers = PastPaper.objects.filter(
        examboard=pastpaper.examboard
    ).count()
    pastpaper_progress_percentage = (
        int(100 * num_pastpapers_completed / total_num_pastpapers)
        if total_num_pastpapers > 0
        else 0
    )
    context = {
        "is_request_htmx": is_request_htmx,
        "pastpaper": pastpaper,
        "examboard": examboard,
        "num_pastpapers_completed": num_pastpapers_completed,
        "total_num_pastpapers": total_num_pastpapers,
        "pastpaper_progress_percentage": pastpaper_progress_percentage,
    }
    return render(request, "revision/snippets/complete_pastpaper_row.html", context)


@login_required
def mark_pastpaper_as_uncomplete(request, pastpaper_id):
    """Update PastPaper as uncomplete for User (update PastPaperCompletion instance)."""
    if request.method != "POST":
        raise Http404
    if (
        not PastPaperCompletion.objects.filter(
            user=request.user, pastpaper__id=pastpaper_id, is_complete=True
        ).exists()
        or PastPaperCompletion.objects.filter(
            user=request.user, pastpaper__id=pastpaper_id, is_complete=False
        ).exists()
    ):
        raise Http404
    is_request_htmx = request.headers.get("HX-Request") == "true"
    pastpaper = PastPaper.objects.select_related(
        "examboard", "examboard__subject", "examboard__subject__qualification"
    ).get(id=pastpaper_id)
    examboard = pastpaper.examboard
    pastpaper_completion = PastPaperCompletion.objects.get(
        user=request.user, pastpaper=pastpaper, is_complete=True
    )
    pastpaper_completion.is_complete = False
    pastpaper_completion.save()
    num_pastpapers_completed = PastPaperCompletion.objects.filter(
        user=request.user, pastpaper__examboard=pastpaper.examboard, is_complete=True
    ).count()
    total_num_pastpapers = PastPaper.objects.filter(
        examboard=pastpaper.examboard
    ).count()
    pastpaper_progress_percentage = (
        int(100 * num_pastpapers_completed / total_num_pastpapers)
        if total_num_pastpapers > 0
        else 0
    )
    context = {
        "is_request_htmx": is_request_htmx,
        "pastpaper": pastpaper,
        "examboard": examboard,
        "num_pastpapers_completed": num_pastpapers_completed,
        "total_num_pastpapers": total_num_pastpapers,
        "pastpaper_progress_percentage": pastpaper_progress_percentage,
    }
    return render(request, "revision/snippets/uncomplete_pastpaper_row.html", context)


@verified_email_required
def notes(
    request, qualification_slug, subject_slug, examboard_slug, topic_id, topic_slug
):
    """Show notes belonging to Topic instance."""
    qualifications = Qualification.objects.order_by("qualification_number")
    topic = Topic.objects.select_related(
        "examboard", "examboard__subject", "examboard__subject__qualification"
    ).get(id=topic_id)
    prev_topic = Topic.objects.filter(examboard=topic.examboard, id__lt=topic.id).last()
    next_topic = Topic.objects.filter(
        examboard=topic.examboard, id__gt=topic.id
    ).first()
    notes_template = "revision/notes/" + (
        slugify(
            f"{topic.examboard.subject.qualification.slug} {topic.examboard.subject.slug} "
            + f"{topic.examboard.slug} {topic.slug}"
        )
        + ".html"
    )
    notes_template_name = [notes_template, "revision/notes/no_notes_yet.html"]
    context = {
        "qualifications": qualifications,
        "topic": topic,
        "prev_topic": prev_topic,
        "next_topic": next_topic,
        "notes_template_name": notes_template_name,
    }
    return render(request, "revision/notes.html", context)


@login_required
def questions(
    request, qualification_slug, subject_slug, examboard_slug, topic_id, topic_slug
):
    """Show past exam questions belonging to Topic instance."""
    topic = Topic.objects.get(id=topic_id)
    return FileResponse(
        open(topic.questions.path, "rb"),
        content_type="application/pdf",
    )


@login_required
def past_paper(
    request,
    qualification_slug,
    subject_slug,
    examboard_slug,
    pastpaper_id,
    pastpaper_name,
):
    """Show paper belonging to PastPaper instance."""
    past_paper = PastPaper.objects.get(id=pastpaper_id)
    return FileResponse(
        open(past_paper.paper.path, "rb"),
        content_type="application/pdf",
    )


@login_required
def model_answers(
    request,
    qualification_slug,
    subject_slug,
    examboard_slug,
    pastpaper_id,
    pastpaper_name,
):
    """Show model answers belonging to PastPaper instance."""
    past_paper = PastPaper.objects.get(id=pastpaper_id)
    return FileResponse(
        open(past_paper.model_answers.path, "rb"),
        content_type="application/pdf",
    )


@login_required
def mark_scheme(
    request,
    qualification_slug,
    subject_slug,
    examboard_slug,
    pastpaper_id,
    pastpaper_name,
):
    """Show official mark scheme belonging to PastPaper instance."""
    past_paper = PastPaper.objects.get(id=pastpaper_id)
    return FileResponse(
        open(past_paper.mark_scheme.path, "rb"),
        content_type="application/pdf",
    )
