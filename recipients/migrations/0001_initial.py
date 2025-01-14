# Generated by Django 5.1.4 on 2025-01-14 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("birthday", "День рождения"),
                            ("anniversary", "Юбилей"),
                            ("wedding", "Свадьба"),
                            ("new_year", "Новый год"),
                            ("women_day", "8 марта"),
                            ("other", "Другое"),
                        ],
                        default="birthday",
                        max_length=20,
                    ),
                ),
                (
                    "relationship",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Мужчина"), ("female", "Женщина")],
                        max_length=10,
                    ),
                ),
                (
                    "age_range",
                    models.CharField(
                        choices=[
                            (0, "0-1"),
                            (2, "2-6"),
                            (7, "7-13"),
                            (14, "14-25"),
                            (26, "26-50"),
                            (51, "51-70"),
                            (71, "71-120"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
