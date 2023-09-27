from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "This command creates superuser"

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(username="admin")
            User.objects.create_superuser("admin", "admin@naver.com", "12")
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        except:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))
