from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)

class AgendaLayout(blocks.StructBlock):
    session = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("time", blocks.CharBlock()),
                ("session_title", blocks.CharBlock()),
                ("language", blocks.CharBlock()),
                (
                    "program",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            [
                                (
                                    "timeline",
                                    blocks.ListBlock(
                                        blocks.StructBlock(
                                            [
                                                (
                                                    "time",
                                                    blocks.CharBlock(required=False),
                                                ),
                                                ("title", blocks.RichTextBlock()),
                                                (
                                                    "description",
                                                    blocks.RichTextBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "speakers",
                                                    blocks.ListBlock(
                                                        blocks.StructBlock(
                                                            [
                                                                
                                                                (
                                                                    "name",
                                                                    blocks.CharBlock(
                                                                        required=False
                                                                    ),
                                                                ),
                                                                (
                                                                    "designation",
                                                                    blocks.CharBlock(
                                                                        required=False
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                ),
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
        template = "componants/speaker_layout.html"

