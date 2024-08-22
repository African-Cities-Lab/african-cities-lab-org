from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Locale

import african_cities_lab


class SectionTitleBlock(blocks.StructBlock):
    content_position = blocks.CharBlock(required=False, help_text="start, center or end")
    section_title = blocks.StructBlock(
        [
            ("title", blocks.CharBlock(required=False)),
            ("text_align", blocks.CharBlock(required=False, help_text="right, center or left")),
        ]
    )
    section_subparagraph = blocks.StructBlock(
        [
            ("subparagraph", blocks.RichTextBlock(required=False)),
            ("text_align", blocks.CharBlock(required=False, help_text="right, center or left")),
        ]
    )

    class Meta:
        template = "home/blocks/section_title.html"


class ParagraphBlock(blocks.StructBlock):
    content_position = blocks.CharBlock(required=False, help_text="start, center or end")
    text_align = blocks.CharBlock(required=False, help_text="center")
    content = blocks.RichTextBlock(required=False)

    class Meta:
        template = "home/blocks/paragraph.html"


class ButtonBlock(blocks.StructBlock):
    button_position = blocks.CharBlock(required=False, help_text="right, center or left")
    button_size = blocks.CharBlock(help_text="btn__small, btn__xxsmall or btn__big")
    button_type = blocks.CharBlock(help_text="btn__primary, btn__secondary or outline__primary")
    button_url = blocks.URLBlock()
    button_label = blocks.CharBlock()

    class Meta:
        template = "home/blocks/button.html"


class MapBlock(blocks.StructBlock):
    iframe = blocks.TextBlock(required=False)

    class Meta:
        template = "home/blocks/map.html"


class BlankSpaceBlock(blocks.StructBlock):
    height = blocks.CharBlock(help_text="Enter empty space height (Note: CSS measurement units allowed).")

    class Meta:
        template = "home/blocks/blank_space.html"


class AgendaBlock(blocks.StructBlock):
    sessions = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("time", blocks.CharBlock(required=False)),
                ("session_title", blocks.CharBlock(required=False)),
                ("language", blocks.CharBlock(required=False)),
                ("moderator_name", blocks.CharBlock(required=False)),
                (
                    "timeline",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("time", blocks.CharBlock(required=False)),
                                ("title", blocks.RichTextBlock(equired=False)),
                                ("description", blocks.RichTextBlock(required=False)),
                                (
                                    "speakers",
                                    blocks.ListBlock(
                                        blocks.StructBlock(
                                            [
                                                ("name", blocks.CharBlock(required=False)),
                                                ("designation", blocks.CharBlock(required=False)),
                                            ]
                                        ),
                                    ),
                                ),
                            ]
                        ),
                    ),
                ),
            ],
        ),
    )

    class Meta:
        template = "home/blocks/agenda.html"


class SpeakersBlock(blocks.StructBlock):
    speakers = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock()),
                ("name", blocks.CharBlock()),
                (
                    "designation",
                    blocks.RichTextBlock(),
                ),
                (
                    "social_links",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("fa_class", blocks.CharBlock(required=False)),
                                ("profile_link", blocks.CharBlock(required=False)),
                            ]
                        ),
                    ),
                ),
                (
                    "biography",
                    blocks.RichTextBlock(required=False),
                ),
            ],
        ),
    )

    class Meta:
        template = "home/blocks/speakers.html"


class InfiniteScrollingTextsBlock(blocks.StructBlock):
    infinite_scrolling_texts = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("content_text", blocks.CharBlock()),
            ],
        ),
    )

    class Meta:
        template = "home/blocks/infinite_scrolling_texts.html"


class ContentBoxesBlock(blocks.StructBlock):
    content_boxes = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("box_title", blocks.CharBlock()),
                ("box_content", blocks.TextBlock(required=False)),
                ("box_link", blocks.URLBlock(required=False)),
            ],
        ),
    )

    class Meta:
        template = "home/blocks/content_boxes.html"


class IconBoxesBlock(blocks.StructBlock):
    icon_boxes = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("icon", ImageChooserBlock()),
                ("title", blocks.CharBlock()),
                ("content", blocks.TextBlock(required=False)),
                ("link", blocks.URLBlock(required=False)),
            ],
        ),
    )

    class Meta:
        template = "home/blocks/icon_box.html"


class CountersBlock(blocks.StructBlock):
    counters = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("counter_number", blocks.IntegerBlock(help_text="Only numerical values allowed.")),
                ("symbol", blocks.CharBlock(required=False)),
                ("counter_units", blocks.CharBlock(help_text="Ex: coffee drinks, projects, clients.")),
            ]
        )
    )

    class Meta:
        template = "home/blocks/counters.html"


class TimelineBlock(blocks.StructBlock):
    timeline = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("date", blocks.CharBlock()),
                ("title", blocks.CharBlock()),
                ("description", blocks.TextBlock(required=False)),
                ("link", blocks.URLBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "home/blocks/timeline.html"


class LabelsBlock(blocks.StructBlock):
    labels_blocks = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock()),
                ("link", blocks.URLBlock(required=False)),
            ],
        )
    )

    class Meta:
        template = "home/blocks/labels_blocks.html"


class ContactsBlock(blocks.StructBlock):
    contacts_card = blocks.StructBlock(
        [
            ("title", blocks.CharBlock(required=False)),
            ("content", blocks.RichTextBlock(required=False)),
        ]
    )
    social_media_card = blocks.StructBlock(
        [
            ("title", blocks.CharBlock(required=False)),
            ("content", blocks.RichTextBlock(required=False)),
        ]
    )

    class Meta:
        template = "home/blocks/contacts_card.html"


class MoocsBlock(blocks.StructBlock):
    class Meta:
        template = "home/blocks/moocs.html"


class WebinarsBlock(blocks.StructBlock):
    class Meta:
        template = "home/blocks/webinars.html"


class FormationsBlock(blocks.StructBlock):
    class Meta:
        template = "home/blocks/formations.html"


class NewsletterFormBlock(blocks.StructBlock):
    class Meta:
        template = "home/blocks/newsletter_form.html"


class DirectorsBlock(blocks.StructBlock):
    directors = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=False)),
                ("name", blocks.CharBlock(required=False)),
                ("institution", blocks.CharBlock(required=False)),
                ("function", blocks.CharBlock(required=False)),
                (
                    "social_links",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("fa_class", blocks.CharBlock(required=False)),
                                ("profile_link", blocks.CharBlock(required=False)),
                            ]
                        ),
                    ),
                ),
                ("biography", blocks.RichTextBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "home/blocks/directors.html"


class CollaboratorsBlock(blocks.StructBlock):
    collaborators = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("name", blocks.CharBlock(required=False)),
                ("function", blocks.CharBlock(required=False)),
                (
                    "social_links",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("fa_class", blocks.CharBlock(required=False)),
                                ("profile_link", blocks.CharBlock(required=False)),
                            ]
                        )
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "home/blocks/collaborators.html"


class HeroBlock(blocks.StructBlock):
    hero_options = blocks.StructBlock(
        [
            ("background_image", ImageChooserBlock(required=False)),
            ("content_position", blocks.CharBlock(required=False, help_text="start, center or end")),
        ]
    )
    banner_title = blocks.CharBlock()
    banner_content = blocks.StreamBlock(
        [
            ("paragraph", ParagraphBlock()),
            ("button", ButtonBlock()),
            ("infinte_scrolling_texts", InfiniteScrollingTextsBlock()),
        ],
        required=False,
    )

    class Meta:
        template = "home/blocks/hero.html"


class SectionPictureBlock(blocks.StructBlock):
    spotlight_image = ImageChooserBlock()
    content = blocks.StreamBlock(
        [
            ("section_title", SectionTitleBlock()),
            ("paragraph", blocks.RichTextBlock(required=False)),
            ("counters", CountersBlock()),
            ("icon_boxes", IconBoxesBlock()),
            ("blank_space", BlankSpaceBlock()),
            ("button", ButtonBlock()),
        ],
        required=False,
    )

    class Meta:
        template = "home/blocks/section_picture.html"


class FeaturedPostsBlock(blocks.StructBlock):
    section_options = blocks.StructBlock(
        [
            ("background_color", blocks.CharBlock(required=False)),
            ("content_position", blocks.CharBlock(required=False, help_text="start, center or end")),
        ]
    )

    content = blocks.StructBlock(
        [
            (
                "section_title",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=False)),
                        ("text_align", blocks.CharBlock(required=False, help_text="right, center or left")),
                    ]
                ),
            ),
            (
                "section_subparagraph",
                blocks.StructBlock(
                    [
                        ("subparagraph", blocks.CharBlock(required=False)),
                        ("text_align", blocks.CharBlock(required=False, help_text="right, center or left")),
                    ]
                ),
            ),
            (
                "posts_type",
                blocks.ChoiceBlock(
                    choices=[
                        ("moocs", _("MOOCs")),
                        ("formations", _("Formations")),
                        ("webinars", _("Webinars")),
                        ("articles", _("Blog articles")),
                    ],
                ),
            ),
            ("number_of_posts", blocks.IntegerBlock(min_value=1)),
            (
                "button",
                blocks.StructBlock(
                    [
                        (
                            "button_position",
                            blocks.ChoiceBlock(
                                choices=[
                                    ("top", _("Top left")),
                                    ("bottom", _("Bottom Center")),
                                ],
                            ),
                        ),
                        ("button_label", blocks.CharBlock(required=False)),
                        ("archive_page_url", blocks.URLBlock(required=False)),
                    ]
                ),
            ),
        ]
    )

    def render(self, value, context):
        # Get current language
        CURRENT_LANG = Locale.get_active()

        # Get last 3 webinars
        latest_webinars = (
            african_cities_lab.home.models.WebinarPage.objects.filter(locale=CURRENT_LANG)
            .live()
            .public()
            .order_by("-first_published_at")[:3]
        )
        # Get last 3 articles
        latest_articles = (
            african_cities_lab.home.models.BlogPage.objects.filter(locale=CURRENT_LANG)
            .live()
            .public()
            .order_by("-first_published_at")[:3]
        )

        # Get last 3 formations
        latest_formations = (
            african_cities_lab.home.models.FormationPage.objects.filter(locale=CURRENT_LANG)
            .live()
            .public()
            .order_by("-first_published_at")[:3]
        )

        # Get latest 6 moocs
        latest_moocs = african_cities_lab.home.models.Mooc.objects.order_by("-start_date")[:6]
        return super().render(
            value,
            context={
                "webinars": latest_webinars,
                "formations": latest_formations,
                "articles": latest_articles,
                "moocs": latest_moocs,
            },
        )

    class Meta:
        template = "home/blocks/featured_posts.html"


class SectionBlock(blocks.StructBlock):
    section_options = blocks.StructBlock(
        [
            ("background_color", blocks.CharBlock(required=False)),
            ("background_image", ImageChooserBlock(required=False)),
        ]
    )
    content = blocks.StreamBlock(
        [
            ("section_title", SectionTitleBlock()),
            ("paragraph", ParagraphBlock()),
            ("button", ButtonBlock()),
            ("map", MapBlock()),
            ("blank_space", BlankSpaceBlock()),
            ("agenda", AgendaBlock()),
            ("speakers", SpeakersBlock()),
            ("infinite_scrolling_texts", InfiniteScrollingTextsBlock()),
            ("content_boxes", ContentBoxesBlock()),
            ("icon_boxes", IconBoxesBlock()),
            ("counters", CountersBlock()),
            ("timeline", TimelineBlock()),
            ("labels", LabelsBlock()),
            ("contacts", ContactsBlock()),
            ("directors_profil", DirectorsBlock()),
            ("collaborators_profil", CollaboratorsBlock()),
        ],
        required=False,
    )

    class Meta:
        template = "home/blocks/section.html"
