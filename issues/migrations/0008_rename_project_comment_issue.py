# Generated by Django 4.2 on 2023-04-28 15:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("issues", "0007_project_owner_alter_contributor_project"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="project",
            new_name="issue",
        ),
    ]
