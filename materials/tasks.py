from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return "Course not found"

    subscriptions = Subscription.objects.filter(course=course)
    emails = [sub.user.email for sub in subscriptions if sub.user.email]

    if not emails:
        return "No subscribers"

    subject = f"Обновление курса: {course.name}"
    message = f'Здравствуйте!\n\nКурс "{course.name}" был обновлён. Проверьте новые материалы.'

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=False,
    )

    return f"Sent to {len(emails)} users"
