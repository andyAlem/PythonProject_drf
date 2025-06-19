from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает группы пользователей"

    def handle(self, *args, **options):
        for group_name in ["moders", "admins"]:
            Group.objects.get_or_create(name=group_name)
        self.stdout.write(self.style.SUCCESS("Группы успешно созданы."))
