# Generated by Django 5.1.2 on 2024-10-20 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="user",
            new_name="author",
        ),
    ]
