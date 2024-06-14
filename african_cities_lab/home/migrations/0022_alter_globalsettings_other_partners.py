# Generated by Django 4.2.9 on 2024-06-13 19:36

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0021_alter_globalsettings_other_partners"),
    ]

    operations = [
        migrations.AlterField(
            model_name="globalsettings",
            name="other_partners",
            field=wagtail.fields.StreamField(
                [
                    (
                        "partners",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "partner",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "logo",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "organisation_url",
                                                    wagtail.blocks.URLBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]