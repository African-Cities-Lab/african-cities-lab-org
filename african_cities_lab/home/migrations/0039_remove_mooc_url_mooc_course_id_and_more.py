# Generated by Django 4.2.9 on 2024-08-29 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0038_alter_eventindexpage_body_alter_homepage_body"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mooc",
            name="url",
        ),
        migrations.AddField(
            model_name="mooc",
            name="course_id",
            field=models.CharField(default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="logo_url",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="organization",
            name="short_name",
            field=models.CharField(max_length=50),
        ),
    ]
