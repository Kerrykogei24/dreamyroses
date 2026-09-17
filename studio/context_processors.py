from django.conf import settings


def brand(request):
    """Makes shop contact details available in every template as {{ brand.x }}."""
    return {"brand": settings.BRAND}
