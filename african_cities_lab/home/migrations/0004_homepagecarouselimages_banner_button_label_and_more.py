# Generated by Django 4.2.9 on 2024-04-12 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_alter_flatpage_body_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepagecarouselimages",
            name="banner_button_label",
            field=models.CharField(default="Learn more"),
        ),
        migrations.AlterField(
            model_name="homepagecarouselimages",
            name="banner_cta",
            field=models.URLField(help_text="Put URL here"),
        ),
    ]
