# Generated by Django 4.2.5 on 2023-10-07 05:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="room",
            options={"verbose_name_plural": "방 목록"},
        ),
    ]
