from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "This command creates superuser"

    def handle(self, *args, **options):
        try:
            User.objects.get(username="admin")
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))
        except:
            User.objects.create_superuser("admin", "admin@naver.com", "12")
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
