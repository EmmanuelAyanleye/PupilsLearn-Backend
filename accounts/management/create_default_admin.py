import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create a default superuser from environment variables if none exists"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("A superuser already exists. Skipping creation.")
            return

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.role = User.ROLE_ADMIN
            user.set_password(password)
            user.save()
            self.stdout.write(f"Promoted existing user {username} to superuser.")
            return

        User.objects.create_superuser(username=username, email=email, password=password, role=User.ROLE_ADMIN)
        self.stdout.write(f"Created superuser {username} with email {email}. Please change the password now.")
