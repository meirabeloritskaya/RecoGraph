from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recipients.models import Recipients
import json


class Command(BaseCommand):
    help = "Import users and recipients from JSON file"

    def handle(self, *args, **kwargs):
        file_path = "C:/Users/Meira/PycharmProjects/RecoGraph/recipients/data/users_and_recipients.json"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                User = get_user_model()

                for user_data in data["users"]:
                    user, created = User.objects.get_or_create(
                        email=user_data["email"],
                        defaults={"password": user_data["password"]},
                    )
                    if created:
                        self.stdout.write(f"User '{user.email}' created.")
                    else:
                        self.stdout.write(f"User '{user.email}' already exists.")

                    for recipient_data in user_data.get("recipients", []):
                        recipient, rec_created = Recipients.objects.get_or_create(
                            user=user,
                            # relationship=recipient_data['relationship'],
                            # event_type=recipient_data['event_type'],
                            gender=recipient_data["gender"],
                            age_range=recipient_data["age_range"],
                            price_range=recipient_data["price_range"],
                        )
                        if rec_created:
                            self.stdout.write(
                                f"Recipient for user '{user.email}' created."
                            )
                        else:
                            self.stdout.write(
                                f"Recipient for user '{user.email}' already exists."
                            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR("File not found. Please check the file path.")
            )
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format."))
