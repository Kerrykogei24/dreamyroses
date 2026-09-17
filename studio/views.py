from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import EnquiryForm
from .models import Drawing


def home(request):
    featured = Drawing.objects.filter(is_featured=True)[:6]
    if not featured:
        featured = Drawing.objects.all()[:6]
    return render(request, "pages/home.html", {"featured": featured})


def about(request):
    return render(request, "pages/about.html")


def drawings(request):
    """Gallery, optionally narrowed with ?style=anime."""
    style = request.GET.get("style", "")
    pages = Drawing.objects.all()
    valid_styles = dict(Drawing.Style.choices)
    if style in valid_styles:
        pages = pages.filter(style=style)
    else:
        style = ""
    return render(
        request,
        "pages/drawings.html",
        {
            "pages": pages,
            "styles": Drawing.Style.choices,
            "active_style": style,
            "total": Drawing.objects.count(),
        },
    )


def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                # Silently accept and discard so bots learn nothing.
                messages.success(request, "Thank you. Your message is on its way.")
                return redirect("studio:contact")

            enquiry = form.save()
            send_mail(
                subject=f"New enquiry from {enquiry.name} — {enquiry.get_interest_display()}",
                message=(
                    f"Name: {enquiry.name}\n"
                    f"Email: {enquiry.email}\n"
                    f"Phone: {enquiry.phone or '—'}\n"
                    f"Interest: {enquiry.get_interest_display()}\n\n"
                    f"{enquiry.message}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ORDER_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
            messages.success(
                request,
                f"Thank you, {enquiry.name}. Miriam usually replies within a day.",
            )
            return redirect("studio:contact")
        messages.error(request, "Check the highlighted fields and send again.")
    else:
        form = EnquiryForm()
    return render(request, "pages/contact.html", {"form": form})
