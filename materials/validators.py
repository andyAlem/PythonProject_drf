from urllib.parse import \
    urlparse  # https://docs.python.org/3/library/urllib.parse.html

from rest_framework.serializers import ValidationError

allowed_domains = ["youtube.com", "www.youtube.com"]


def validate_forbidden_links(value):
    """Проверка ссылки на youtube.com"""
    try:
        domain = urlparse(value).netloc.lower()
    except Exception:
        raise ValidationError("Можно добавлять видео только из youtube.com")

    if domain not in allowed_domains:
        raise ValidationError("Разрешены только ссылки на youtube.com")
