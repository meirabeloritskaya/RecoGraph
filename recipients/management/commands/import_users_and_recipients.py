import json
from django.core.management.base import BaseCommand
from users.models import User
from recipients.models import Recipients


class Command(BaseCommand):
    help = 'Import users and their recipients from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = 'recipients/data/users_and_recipients.json'

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for user_data in data['users']:
            email = user_data['email']
            password = user_data['password']

            # Создаём пользователя
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.set_password(password)
                user.save()

            # Создаём получателей
            for recipient_data in user_data['recipients']:
                Recipients.objects.create(
                    user=user,
                    event_type=recipient_data['event_type'],
                    relationship=recipient_data.get('relationship'),
                    gender=recipient_data['gender'],
                    age_range=recipient_data['age_range']
                )

        self.stdout.write(self.style.SUCCESS('Users and recipients imported successfully!'))
