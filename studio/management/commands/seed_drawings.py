"""Load the studio's sample pages into the gallery.

    python manage.py seed_drawings

Safe to run more than once: existing pages with the same slug are left alone.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from studio.models import Drawing

SAMPLES = [
    ("sample-graduation.jpg", "Graduation day", Drawing.Style.MILESTONE,
     "Gown open, arms out, the whole campus behind her.", True),
    ("sample-best-friends.jpg", "Two of us", Drawing.Style.FRIENDS,
     "Braids and curls, cheek to cheek.", True),
    ("sample-road-trip.jpg", "Back seat", Drawing.Style.PORTRAIT,
     "A patched jacket and a long drive.", True),
    ("sample-poolside.jpg", "Stepping stones", Drawing.Style.PORTRAIT,
     "Halfway across, arms out for balance.", True),
    ("sample-daydream.jpg", "Chin in hand", Drawing.Style.PORTRAIT,
     "A quiet afternoon, drawn in soft lines.", True),
    ("sample-hoodie-moment.jpg", "Caught laughing", Drawing.Style.ANIME,
     "Drawn in the anime style the studio is known for.", True),
    ("sample-feet-in-water.jpg", "Feet in the water", Drawing.Style.PORTRAIT,
     "Slides kicked off at the edge of the pool.", False),
    ("sample-heart-cheeks.jpg", "Hearts on her cheeks", Drawing.Style.PORTRAIT,
     "A birthday portrait with painted hearts.", False),
    ("sample-in-the-park.jpg", "Afternoon in the park", Drawing.Style.PORTRAIT,
     "Trees, grass and a good pair of jeans.", False),
]


class Command(BaseCommand):
    help = "Load the sample coloring pages shipped with the project into the gallery."

    def handle(self, *args, **options):
        source_dir = Path(settings.BASE_DIR) / "static" / "img" / "samples"
        created = 0

        for position, (filename, title, style, caption, featured) in enumerate(SAMPLES):
            if Drawing.objects.filter(title=title).exists():
                self.stdout.write(f"skipped (already there): {title}")
                continue

            path = source_dir / filename
            if not path.exists():
                self.stderr.write(f"missing file: {path}")
                continue

            drawing = Drawing(
                title=title,
                style=style,
                caption=caption,
                is_featured=featured,
                position=position,
            )
            with path.open("rb") as fh:
                drawing.image.save(filename, File(fh), save=False)
            drawing.save()
            created += 1
            self.stdout.write(f"added: {title}")

        self.stdout.write(self.style.SUCCESS(f"Done. {created} page(s) added."))
