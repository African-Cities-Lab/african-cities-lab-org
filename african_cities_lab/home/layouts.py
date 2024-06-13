from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class SectionTitleLayout(blocks.StructBlock):
    text_align = blocks.CharBlock(required=False, help_text="center")
    section_title = blocks.CharBlock()
    section_subparagraph = blocks.TextBlock(required=False)

    class Meta:
        template = "components/section_title_layout.html"


class ParagraphLayout(blocks.StructBlock):
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
        template = "components/paragraph_layout.html"


class Button(blocks.StructBlock):
    button_position = blocks.CharBlock(required=False, help_text="center")
    button_size = blocks.CharBlock(help_text="btn__small, btn__xxsmall or btn__big")
    button_type = blocks.CharBlock(help_text="btn__primary, btn__secondary or outline__primary")
    button_url = blocks.URLBlock()
    button_label = blocks.CharBlock()

    class Meta:
        template = "components/button.html"


class Map(blocks.StructBlock):
    iframe = blocks.TextBlock(required=False)

    class Meta:
        template = "components/map.html"


class BlankSpace(blocks.StructBlock):
    height = blocks.CharBlock(help_text="Enter empty space height (Note: CSS measurement units allowed).")

    class Meta:
        template = "components/blank_space.html"


class AgendaLayout(blocks.StructBlock):
    session = blocks.ListBlock(
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
        template = "components/agenda_layout.html"


class SpeakerLayout(blocks.StructBlock):
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
        template = "components/speaker_layout.html"


class InfiniteScrollingText(blocks.StructBlock):
    infinite_scrolling_text = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("content_text", blocks.CharBlock()),
            ],
        ),
    )

    class Meta:
        template = "components/infinite_scrolling_text.html"


class ContentBox(blocks.StructBlock):
    content_box = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("box_title", blocks.CharBlock()),
                ("box_content", blocks.TextBlock(required=False)),
                ("box_link", blocks.URLBlock(required=False)),
            ],
        ),
    )

    class Meta:
        template = "components/content_box_layout.html"


class IconBox(blocks.StructBlock):
    icon_box = blocks.ListBlock(
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
        template = "components/icon_box_layout.html"


class Counter(blocks.StructBlock):
    counter = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("counter_number", blocks.IntegerBlock(help_text="Only numerical values allowed.")),
                ("symbol", blocks.CharBlock(required=False)),
                ("counter_units", blocks.CharBlock(help_text="Ex: coffee drinks, projects, clients.")),
            ]
        )
    )

    class Meta:
        template = "components/counter_layout.html"


class Timeline(blocks.StructBlock):
    timeline_item = blocks.ListBlock(
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
        template = "components/timeline_layout.html"


class Section(blocks.StructBlock):
    section = blocks.ListBlock(
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
        template = "components/row_layout.html"
