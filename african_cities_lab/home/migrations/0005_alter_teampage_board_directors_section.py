# Generated by Django 4.2.9 on 2024-04-12 17:36

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_homepagecarouselimages_banner_button_label_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teampage",
            name="board_directors_section",
            field=wagtail.fields.StreamField(
                [
                    (
                        "board",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "sub_paragraph",
                                    wagtail.blocks.RichTextBlock(required=False),
                                ),
                                (
                                    "board_director",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "name",
                                                    wagtail.blocks.CharBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "institution",
                                                    wagtail.blocks.CharBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "function",
                                                    wagtail.blocks.CharBlock(
                                                        required=False
                                                    ),
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
