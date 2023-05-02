# Generated by Django 4.2 on 2023-05-02 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("issues", "0009_alter_contributor_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="assignee",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assignee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]