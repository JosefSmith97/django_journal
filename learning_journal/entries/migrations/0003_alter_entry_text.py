# Generated by Django 4.1.2 on 2023-01-23 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entries", "0002_alter_entry_options_alter_entry_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="text",
            field=models.TextField(blank=True),
        ),
    ]
