# Generated by Django 4.2.3 on 2023-10-06 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_article_owner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="owner",
        ),
    ]