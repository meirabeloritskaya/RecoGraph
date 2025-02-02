from django.db import models


class Recipients(models.Model):

    # EVENT_TYPES = [
    #     ('birthday', 'День рождения'),
    #     ('anniversary', 'Юбилей'),
    #     ('wedding', 'Свадьба'),
    #     ('new_year', 'Новый год'),
    #     ('women_day', '8 марта'),
    #     ('other', 'Другое'),
    # ]

    GENDER_CHOICES = [
        ("male", "Мужчина"),
        ("female", "Женщина"),
    ]

    AGE_RANGE_CHOICES = [
        (0, "0-1"),
        (2, "2-6"),
        (7, "7-13"),
        (14, "14-25"),
        (26, "26-50"),
        (51, "51-70"),
        (71, "71-120"),
    ]

    # RELATIONSHIPS = [
    #     ('mother', 'Мама/Папа'),
    #     ('wife', 'Жена/Муж'),
    #     ('daughter', 'Дочь/Сын'),
    #     ('sister', 'Сестра/Брат'),
    #     ('grandmother', 'Бабушка/Дедушка'),
    #     ('friend', 'Подруга/Друг'),
    #     ('other', 'Другое'),
    # ]

    PRICE_RANGE = [
        ("100-1500", "100-1500 руб."),
        ("1501-5000", "1501-5000 руб."),
        ("5001-10000", "5001-10000 руб."),
        ("10001-50000", "10001-50000 руб."),
        ("50001-100000", "50001-100000 руб."),
        ("100001-200000", "100001-200000 руб."),
    ]

    price_range = models.CharField(
        max_length=25,
        choices=PRICE_RANGE,
        blank=True,
        null=True,
        help_text="Желаемый диапазон цен для подарка",
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="recipients"
    )  # Связь с пользователем
    # event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='birthday', blank=True, null=True)
    # relationship = models.CharField(max_length=20, choices=RELATIONSHIPS, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default="male"
    )  # Пол обязателен
    age_range = models.CharField(
        max_length=20, choices=AGE_RANGE_CHOICES, default=14
    )  # Диапазон возраста обязателен

    def __str__(self):
        return f"{self.user} - {self.event_type} ({self.relationship if self.relationship else 'Нет отношения'})"
