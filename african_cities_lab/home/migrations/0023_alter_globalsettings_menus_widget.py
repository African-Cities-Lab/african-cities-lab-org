# Generated by Django 4.2.9 on 2024-06-13 21:59

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0022_alter_globalsettings_other_partners"),
    ]

    operations = [
        migrations.AlterField(
            model_name="globalsettings",
            name="menus_widget",
            field=wagtail.fields.StreamField(
                [
                    (
                        "widgets",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "menu_widget",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "widget_title_en",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Add content in english",
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "widget_title_fr",
                                                    wagtail.blocks.CharBlock(
                                                        help_text="Add content in french",
                                                        required=False,
                                                    ),
                                                ),
                                                (
                                                    "flat_menu",
                                                    wagtail.blocks.ChoiceBlock(
                                                        choices=[
                                                            (
                                                                "footer_menu_1",
                                                                "Footermenu 1",
                                                            ),
                                                            (
                                                                "footer_menu_2",
                                                                "Footermenu 2",
                                                            ),
                                                            (
                                                                "footer_menu_3",
                                                                "Footermenu 3",
                                                            ),
                                                        ],
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
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]