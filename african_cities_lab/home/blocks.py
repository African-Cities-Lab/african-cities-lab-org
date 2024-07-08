from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class SectionTitleBlock(blocks.StructBlock):
    text_align = blocks.CharBlock(required=False, help_text="center")
    section_title = blocks.CharBlock()
    section_subparagraph = blocks.TextBlock(required=False)

    class Meta:
        template = "home/blocks/section_title.html"


class ParagraphBlock(blocks.StructBlock):
    text_align = blocks.CharBlock(required=False, help_text="center")
    content = blocks.StreamBlock(
        [
            (
                "block",
                blocks.RichTextBlock(),
            ),
        ],
    )

    class Meta:
        template = "home/blocks/paragraph.html"


class ButtonBlock(blocks.StructBlock):
    button_position = blocks.CharBlock(required=False, help_text="center")
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


class BannerImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    banner_title = blocks.CharBlock()
    infinte_scrolling_texts = InfiniteScrollingTextsBlock(required=False)

    class Meta:
        template = "home/blocks/banner_image.html"


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


class SectionsBlock(blocks.StructBlock):
    sections = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("background_color", blocks.CharBlock(required=False)),
                ("background_image", ImageChooserBlock(required=False)),
                ("title", blocks.CharBlock()),
                ("paragraph", blocks.RichTextBlock(required=False)),
                ("link", blocks.URLBlock(required=False)),
                ("content_alignement", blocks.CharBlock(required=False, help_text="center")),
            ]
        )
    )

    class Meta:
        template = "home/blocks/sections.html"


class OffersBlock(blocks.StructBlock):
    offers = blocks.StructBlock(
        [
            ("heading", blocks.CharBlock(required=False)),
            ("sub_paragraph", blocks.RichTextBlock(required=False)),
            (
                "icon_box",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("icon", ImageChooserBlock(required=False)),
                            ("title", blocks.CharBlock(required=False)),
                            ("content", blocks.TextBlock(required=False)),
                        ],
                    ),
                ),
            ),
        ]
    )

    class Meta:
        template = "home/blocks/offers.html"


class FocusAreasBlock(blocks.StructBlock):
    focus_areas = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("heading", blocks.CharBlock(required=False)),
                ("sub_paragraph", blocks.RichTextBlock(required=False)),
                (
                    "items",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                ("title", blocks.CharBlock()),
                                (
                                    "link",
                                    blocks.URLBlock(required=False),
                                ),
                            ],
                        ),
                    ),
                ),
            ]
        )
    )

    class Meta:
        template = "home/blocks/focus_areas.html"


class MissionBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(required=False)
    subtitle = blocks.TextBlock(required=False)
    paragraph = blocks.RichTextBlock(required=False)
    counters = CountersBlock()

    class Meta:
        template = "home/blocks/mission.html"


class ContactsBlock(blocks.StructBlock):
    section_title = blocks.CharBlock(required=False)
    paragraph = blocks.TextBlock(required=False)
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


class AdditionalInformationBlock(blocks.StructBlock):
    additional_informations = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("section_title", SectionTitleBlock()),
                ("paragraph", ParagraphBlock()),
                ("button", ButtonBlock()),
                ("content_boxes", ContentBoxesBlock()),
                ("icon_boxes", IconBoxesBlock()),
                ("map", MapBlock()),
                ("blank_space", BlankSpaceBlock()),
            ],
        )
    )


class OverviewsBlock(blocks.StructBlock):
    overviews = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=False)),
                ("heading", blocks.CharBlock(required=False)),
                ("paragraph", blocks.RichTextBlock(required=False)),
            ]
        ),
    )


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
