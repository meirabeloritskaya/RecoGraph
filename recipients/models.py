from django.db import models


class Recipients(models.Model):

    EVENT_TYPES = [
        ('birthday', 'День рождения'),
        ('anniversary', 'Юбилей'),
        ('wedding', 'Свадьба'),
        ('new_year', 'Новый год'),
        ('women_day', '8 марта'),
        ('other', 'Другое'),
    ]

    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    ]

    AGE_RANGE_CHOICES = [
        (0, '0-1'),
        (2, '2-6'),
        (7, '7-13'),
        (14, '14-25'),
        (26, '26-50'),
        (51, '51-70'),
        (71, '71-120'),
    ]

    FEMALE_RELATIONSHIPS = [
        ('mother', 'Мама'),
        ('wife', 'Жена'),
        ('daughter', 'Дочь'),
        ('sister', 'Сестра'),
        ('grandmother', 'Бабушка'),
        ('friend', 'Подруга'),
        ('other', 'Другое'),
    ]

    MALE_RELATIONSHIPS = [
        ('father', 'Папа'),
        ('husband', 'Муж'),
        ('son', 'Сын'),
        ('brother', 'Брат'),
        ('grandfather', 'Дедушка'),
        ('friend', 'Друг'),
        ('other', 'Другое'),
    ]
    PRICE_RANGE = [
        ('low', 'До 20$'),
        ('medium', '20$ - 50$'),
        ('high', '50$ - 100$'),
        ('premium', 'Более 100$'),
    ]

    price_range = models.CharField(max_length=10, choices=PRICE_RANGE, blank=True, null=True, help_text="Желаемый диапазон цен для подарка")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)  # Связь с пользователем
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='birthday')
    relationship = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # Пол обязателен
    age_range = models.CharField(max_length=20, choices=AGE_RANGE_CHOICES)  # Диапазон возраста обязателен

    def __str__(self):
        return f"{self.user} - {self.event_type} ({self.relationship if self.relationship else 'Нет отношения'})"
