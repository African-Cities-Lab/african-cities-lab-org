# Generated by Django 4.2.9 on 2024-03-18 12:49

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_alter_webinarpage_body_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="webinarpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "agenda_layout",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "session",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                ("time", wagtail.blocks.CharBlock()),
                                                (
                                                    "session_title",
                                                    wagtail.blocks.CharBlock(),
                                                ),
                                                (
                                                    "language",
                                                    wagtail.blocks.CharBlock(),
                                                ),
                                                (
                                                    "program",
                                                    wagtail.blocks.ListBlock(
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "timeline",
                                                                    wagtail.blocks.ListBlock(
                                                                        wagtail.blocks.StructBlock(
                                                                            [
                                                                                (
                                                                                    "time",
                                                                                    wagtail.blocks.CharBlock(
                                                                                        required=False
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "title",
                                                                                    wagtail.blocks.RichTextBlock(),
                                                                                ),
                                                                                (
                                                                                    "description",
                                                                                    wagtail.blocks.RichTextBlock(
                                                                                        required=False
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "speakers",
                                                                                    wagtail.blocks.ListBlock(
                                                                                        wagtail.blocks.StructBlock(
                                                                                            [
                                                                                                (
                                                                                                    "name",
                                                                                                    wagtail.blocks.CharBlock(
                                                                                                        required=False
                                                                                                    ),
                                                                                                ),
                                                                                                (
                                                                                                    "designation",
                                                                                                    wagtail.blocks.CharBlock(
                                                                                                        required=False
                                                                                                    ),
                                                                                                ),
                                                                                            ]
                                                                                        )
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ),
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "speaker_layout",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "speakers",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(),
                                                ),
                                                ("name", wagtail.blocks.CharBlock()),
                                                (
                                                    "designation",
                                                    wagtail.blocks.RichTextBlock(),
                                                ),
                                                (
                                                    "social_links",
                                                    wagtail.blocks.ListBlock(
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "fa_class",
                                                                    wagtail.blocks.CharBlock(
                                                                        required=False
                                                                    ),
                                                                ),
                                                                (
                                                                    "profile_link",
                                                                    wagtail.blocks.CharBlock(
                                                                        required=False
                                                                    ),
                                                                ),
                                                            ]
                                                        )
                                                    ),
                                                ),
                                                (
                                                    "biography",
                                                    wagtail.blocks.RichTextBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    ),
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]