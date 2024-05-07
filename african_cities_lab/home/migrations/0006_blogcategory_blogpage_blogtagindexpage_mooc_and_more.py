# Generated by Django 4.2.9 on 2024-05-07 11:05

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.fields
import wagtailmetadata.models


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("home", "0005_alter_teampage_board_directors_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "language",
                    models.TextField(
                        choices=[("English", "English"), ("French", "French")],
                        default="English",
                        max_length=10,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        help_text="A slug to identify posts by this category",
                        max_length=255,
                        null=True,
                        verbose_name="slug",
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog Category",
                "verbose_name_plural": "blog categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="BlogPage",
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
                ("date", models.DateField(verbose_name="Post date")),
                ("body", wagtail.fields.RichTextField(blank=True)),
                (
                    "categories",
                    modelcluster.fields.ParentalManyToManyField(
                        blank=True, to="home.blogcategory"
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
            name="BlogTagIndexPage",
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
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="Mooc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField()),
                ("url", models.SlugField(unique=True)),
                ("organisation", models.CharField()),
                ("course_image", models.ImageField(null=True, upload_to="moocs")),
                ("start_date", models.CharField(max_length=50)),
                ("start_display", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="BlogPageTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content_object",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tagged_items",
                        to="home.blogpage",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_items",
                        to="taggit.tag",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="blogpage",
            name="tags",
            field=modelcluster.contrib.taggit.ClusterTaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="home.BlogPageTag",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.CreateModel(
            name="BlogIndexPage",
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
                "verbose_name": "Blog Index Page",
            },
            bases=(
                wagtailmetadata.models.WagtailImageMetadataMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
    ]
