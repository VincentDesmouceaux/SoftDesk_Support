# Generated by Django 5.1.4 on 2024-12-18 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"ordering": ["id"]},
        ),
    ]