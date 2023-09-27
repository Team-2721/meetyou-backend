from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="maycan_official@naver.com")
        if not admin:
            User.objects.create_superuser("admin", "admin@naver.com", "12")
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))
