# Generated by Django 4.2.9 on 2024-06-12 15:26

from django.db import migrations, models
import django.db.models.deletion
import wagtailmetadata.models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("home", "0015_alter_contactpage_additional_informations_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsletterPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "banner_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "search_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Search image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Newsletter Page",
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
    ]
