import json
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import users from JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="Path to the JSON file with users"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        User = get_user_model()

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                users = data.get("users", [])
                if not users:
                    self.stdout.write(self.style.WARNING("No users found in the file"))
                    return

                for user_data in users:
                    email = user_data.get("email")
                    password = user_data.get("password")

                    if not email or not password:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Skipping user with incomplete data: {user_data}"
                            )
                        )
                        continue

                    if User.objects.filter(email=email).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f"User with email {email} already exists"
                            )
                        )
                        continue

                    User.objects.create_user(email=email, password=password)
                    self.stdout.write(
                        self.style.SUCCESS(f"User {email} created successfully")
                    )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f"Invalid JSON format in file: {file_path}")
            )
