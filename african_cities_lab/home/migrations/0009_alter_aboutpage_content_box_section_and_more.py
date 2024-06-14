# Generated by Django 4.2.9 on 2024-06-10 04:32

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_aboutpage_content_box_section_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aboutpage",
            name="content_box_section",
            field=wagtail.fields.StreamField(
                [
                    (
                        "content_box",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "subtitle",
                                    wagtail.blocks.RichTextBlock(required=False),
                                ),
                                (
                                    "content_box",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "content_box",
                                                wagtail.blocks.ListBlock(
                                                    wagtail.blocks.StructBlock(
                                                        [
                                                            (
                                                                "box_title",
                                                                wagtail.blocks.CharBlock(),
                                                            ),
                                                            (
                                                                "box_content",
                                                                wagtail.blocks.TextBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                            (
                                                                "box_link",
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
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="aboutpage",
            name="section_layout",
            field=wagtail.fields.StreamField(
                [
                    (
                        "section",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "section",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "section",
                                                wagtail.blocks.ListBlock(
                                                    wagtail.blocks.StructBlock(
                                                        [
                                                            (
                                                                "background_color",
                                                                wagtail.blocks.CharBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                            (
                                                                "background_image",
                                                                wagtail.images.blocks.ImageChooserBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                            (
                                                                "title",
                                                                wagtail.blocks.CharBlock(),
                                                            ),
                                                            (
                                                                "paragraph",
                                                                wagtail.blocks.TextBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                            (
                                                                "link",
                                                                wagtail.blocks.URLBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                            (
                                                                "content_alignement",
                                                                wagtail.blocks.CharBlock(
                                                                    help_text="center",
                                                                    required=False,
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                ),
                                            )
                                        ]
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
        migrations.AlterField(
            model_name="aboutpage",
            name="timeline_section",
            field=wagtail.fields.StreamField(
                [
                    (
                        "timeline",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "subtitle",
                                    wagtail.blocks.RichTextBlock(required=False),
                                ),
                                (
                                    "timeline_item",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "timeline_item",
                                                wagtail.blocks.ListBlock(
                                                    wagtail.blocks.StructBlock(
                                                        [
                                                            (
                                                                "date",
                                                                wagtail.blocks.CharBlock(),
                                                            ),
                                                            (
                                                                "title",
                                                                wagtail.blocks.CharBlock(),
                                                            ),
                                                            (
                                                                "description",
                                                                wagtail.blocks.TextBlock(
                                                                    required=False
                                                                ),
                                                            ),
                                                            (
                                                                "link",
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
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]