from django.db import models
from django.utils.text import slugify


class Drawing(models.Model):
    """A finished coloring page shown in the drawings gallery."""

    class Style(models.TextChoices):
        PORTRAIT = "portrait", "Portrait"
        COUPLE = "couple", "Couple"
        FAMILY = "family", "Family"
        FRIENDS = "friends", "Friends"
        ANIME = "anime", "Anime"
        MILESTONE = "milestone", "Milestone"

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    style = models.CharField(max_length=20, choices=Style.choices, default=Style.PORTRAIT)
    image = models.ImageField(upload_to="drawings/")
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="One line about the photo this page came from.",
    )
    is_featured = models.BooleanField(
        default=False, help_text="Featured pages appear on the landing page."
    )
    position = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first."
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:130] or "drawing"
            slug, n = base, 2
            while Drawing.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Enquiry(models.Model):
    """A message sent from the contact page."""

    class Interest(models.TextChoices):
        PERSONALISED = "personalised", "A personalised coloring book"
        SINGLE_PAGE = "single_page", "A single coloring page"
        GIFT = "gift", "A gift for someone"
        BULK = "bulk", "Bulk or event order"
        OTHER = "other", "Something else"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    interest = models.CharField(
        max_length=20, choices=Interest.choices, default=Interest.PERSONALISED
    )
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} — {self.get_interest_display()}"
