# Generated by Django 4.1.2 on 2022-12-15 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entries", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="entry",
            options={"verbose_name": "Entry", "verbose_name_plural": "Entries"},
        ),
        migrations.AlterField(
            model_name="entry",
            name="date",
            field=models.DateTimeField(),
        ),
    ]