# Generated by Django 4.2.9 on 2024-06-07 13:52

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_blogcategory_blogpage_blogtagindexpage_mooc_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="focus_areas_section",
            field=wagtail.fields.StreamField(
                [
                    (
                        "focus_areas",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "sub_paragraph",
                                    wagtail.blocks.RichTextBlock(required=False),
                                ),
                                (
                                    "items",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                ("title", wagtail.blocks.CharBlock()),
                                                (
                                                    "link",
                                                    wagtail.blocks.URLBlock(
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
        migrations.AddField(
            model_name="homepage",
            name="offers_section",
            field=wagtail.fields.StreamField(
                [
                    (
                        "our_offers",
                        wagtail.blocks.StructBlock(
                            [
                                ("heading", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "sub_paragraph",
                                    wagtail.blocks.RichTextBlock(required=False),
                                ),
                                (
                                    "icon_box",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "icon",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "title",
                                                    wagtail.blocks.CharBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "content",
                                                    wagtail.blocks.TextBlock(
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
