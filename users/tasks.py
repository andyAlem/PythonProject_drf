from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_inactive_users():
    """функция деактивации пользователей"""
    threshold_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"Deactivated {count} inactive users"
