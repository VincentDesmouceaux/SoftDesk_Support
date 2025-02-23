# Generated by Django 5.1.4 on 2024-12-18 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contributors", "0001_initial"),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributor",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_contributor_links",
                to="projects.project",
            ),
        ),
    ]
