# Generated by Django 4.2.9 on 2024-03-18 10:02

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtailmetadata.models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("home", "0004_moocindexpage_flatpage_contestpage_contactpage_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebinarPage",
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
                ("summary", models.TextField()),
                ("date", models.DateField(verbose_name="Webinar date")),
                ("time", models.CharField(max_length=50, null=True)),
                ("location", models.CharField(max_length=100, null=True)),
                ("register_link", models.URLField()),
                ("replay_link", models.URLField()),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "agenda_layout",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "agenda",
                                            wagtail.blocks.ListBlock(
                                                wagtail.blocks.StructBlock(
                                                    [
                                                        (
                                                            "time",
                                                            wagtail.blocks.CharBlock(),
                                                        ),
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
                            )
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                (
                    "main_image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
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
                "abstract": False,
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="WebinarIndexPage",
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
                "verbose_name": "Webinar Index Page",
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
    ]
