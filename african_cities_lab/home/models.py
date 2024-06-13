from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import (
    Locale,
    Orderable,
    Page,
    TranslatableMixin,
)
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataPageMixin

from african_cities_lab.home.layouts import (
    AgendaLayout,
    BlankSpace,
    Button,
    ContentBox,
    Counter,
    IconBox,
    InfiniteScrollingText,
    Map,
    ParagraphLayout,
    Section,
    SectionTitleLayout,
    SpeakerLayout,
    Timeline,
)


class HomePageCarouselImages(Orderable):
    """Between 1 and 3 images for the home page carousel."""

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = models.TextField(blank=True)
    banner_cta = models.URLField(blank=False, help_text="Put URL here")
    banner_button_label = models.CharField(blank=False, default="Learn more")

    panels = [
        FieldPanel("carousel_image"),
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_cta"),
        FieldPanel("banner_button_label"),
    ]


class HomePage(MetadataPageMixin, Page):
    """HomePage page model."""

    template = "pages/home.html"

    subpage_types = [
        "home.AboutPage",
        "home.MoocIndexPage",
        "home.EventsPage",
        "home.BlogIndexPage",
        "home.WebinarsIndexPage",
        "home.FormationsIndexPage",
        "home.ContestPage",
        "home.ContactPage",
        "home.TeamPage",
        "home.FlatPage",
        "home.NewsletterPage",
    ]

    parent_page_type = [
        "wagtailcore.Page",
    ]
    max_count = 1

    offers_section = StreamField(
        [
            (
                "our_offers",
                blocks.StructBlock(
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
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    focus_areas_section = StreamField(
        [
            (
                "focus_areas",
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
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=3, min_num=1, label="Caroussel Images")],
            heading="Slider",
        ),
        FieldPanel("offers_section"),
        FieldPanel("focus_areas_section"),
    ]

    def get_context(self, request):
        # Get current language
        current_lang = Locale.get_active()

        # Get last 3 webinars
        latest_webinars = (
            WebinarsPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )
        # Get last 3 articles
        latest_articles = (
            BlogPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )
        # Update template context
        context = super().get_context(request)
        context["latest_webinars"] = latest_webinars
        context["latest_articles"] = latest_articles

        return context

    class Meta:
        verbose_name = "Home Page"


class AboutPage(MetadataPageMixin, Page):
    """AboutPage page model."""

    template = "pages/about.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )
    page_title = models.CharField(blank=True, null=True)
    infinite_scrolling_text = StreamField(
        [
            ("infinite_scrolling_text", InfiniteScrollingText()),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    mission_session = StreamField(
        [
            (
                "mission",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock(required=False)),
                        ("title", blocks.CharBlock(required=False)),
                        ("subtitle", blocks.TextBlock(required=False)),
                        ("paragraph", blocks.RichTextBlock(required=False)),
                        ("counter", Counter()),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    content_box_section = StreamField(
        [
            (
                "content_box",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=False)),
                        ("subtitle", blocks.RichTextBlock(required=False)),
                        ("content_box", ContentBox()),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    timeline_section = StreamField(
        [
            (
                "timeline",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=False)),
                        ("subtitle", blocks.RichTextBlock(required=False)),
                        ("timeline_item", Timeline()),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    section_layout = StreamField(
        [
            (
                "section",
                blocks.StructBlock(
                    [
                        ("section", Section()),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("banner_image"), FieldPanel("page_title"), FieldPanel("infinite_scrolling_text")],
            heading="Hero section",
        ),
        FieldPanel("mission_session"),
        FieldPanel("content_box_section"),
        FieldPanel("timeline_section"),
        FieldPanel("section_layout"),
    ]

    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    class Meta:
        verbose_name = "About Page"


class ContestPage(MetadataPageMixin, Page):
    """ContestPage page model."""

    template = "pages/contest.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
    ]

    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    class Meta:
        verbose_name = "Contest Page"


class MoocIndexPage(MetadataPageMixin, Page):
    """MoocIndex page model."""

    template = "pages/moocs_index_page.html"
    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    class Meta:
        verbose_name = "Moocs Page"


class ContactPage(MetadataPageMixin, Page):
    """ContactPage page model."""

    template = "pages/contact.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )

    contacts_informations_section = StreamField(
        [
            (
                "contacts_informations",
                blocks.StructBlock(
                    [
                        ("session_title", blocks.CharBlock(required=False)),
                        ("paragraph", blocks.TextBlock(required=False)),
                        (
                            "contacts_card",
                            blocks.StructBlock(
                                [
                                    ("title", blocks.CharBlock(required=False)),
                                    ("content", blocks.RichTextBlock(required=False)),
                                ]
                            ),
                        ),
                        (
                            "social_media_card",
                            blocks.StructBlock(
                                [
                                    ("title", blocks.CharBlock(required=False)),
                                    ("content", blocks.RichTextBlock(required=False)),
                                ]
                            ),
                        ),
                    ]
                ),
            )
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    additional_informations_section = StreamField(
        [
            ("section_title_layout", SectionTitleLayout()),
            ("paragraph_layout", ParagraphLayout()),
            ("button", Button()),
            ("content_box", ContentBox()),
            ("icon_box", IconBox()),
            ("map", Map()),
            ("blank_space", BlankSpace()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
        FieldPanel("contacts_informations_section"),
        FieldPanel("additional_informations_section"),
    ]

    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    class Meta:
        verbose_name = "Contact Page"


class TeamPage(MetadataPageMixin, Page):
    """TeamPage page model."""

    template = "pages/team.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )

    overview_section = StreamField(
        [
            (
                "overview",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock(required=False)),
                        ("heading", blocks.CharBlock(required=False)),
                        ("paragraph", blocks.RichTextBlock(required=False)),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    board_directors_section = StreamField(
        [
            (
                "board",
                blocks.StructBlock(
                    [
                        ("heading", blocks.CharBlock(required=False)),
                        ("sub_paragraph", blocks.RichTextBlock(required=False)),
                        (
                            "board_director",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        ("image", ImageChooserBlock(required=False)),
                                        ("name", blocks.CharBlock(required=False)),
                                        ("institution", blocks.CharBlock(required=False)),
                                        (
                                            "function",
                                            blocks.CharBlock(required=False),
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
                            ),
                        ),
                    ]
                ),
            ),
        ],
        min_num=1,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    collaborators_section = StreamField(
        [
            (
                "collaborators",
                blocks.StructBlock(
                    [
                        ("heading", blocks.CharBlock(required=False)),
                        ("sub_paragraph", blocks.RichTextBlock(required=False)),
                        (
                            "collaborator",
                            blocks.ListBlock(
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
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ),
                    ]
                ),
            ),
        ],
        min_num=1,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
        FieldPanel("overview_section"),
        FieldPanel("board_directors_section"),
        FieldPanel("collaborators_section"),
    ]

    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    class Meta:
        verbose_name = "Team Page"


class FlatPage(MetadataPageMixin, Page):
    """FlatPage page model."""

    template = "pages/flat_page.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    body = StreamField(
        [
            ("section_title_layout", SectionTitleLayout()),
            ("paragraph_layout", ParagraphLayout()),
            ("button", Button()),
            ("infinite_scrolling_text", InfiniteScrollingText()),
            ("counter", Counter()),
            ("content_box", ContentBox()),
            ("icon_box", IconBox()),
            ("timeline_item", Timeline()),
            ("map", Map()),
            ("blank_space", BlankSpace()),
            ("speaker_layout", SpeakerLayout()),
            ("agenda_layout", AgendaLayout()),
        ],
        blank=True,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
        FieldPanel("body"),
    ]
    parent_page_type = [
        "home.HomePage",
    ]

    class Meta:
        verbose_name = "Flat Page"


class EventsPage(MetadataPageMixin, Page):
    """EventsPage page model."""

    template = "pages/events_page.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
    ]
    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    def get_context(self, request):
        # Get current language
        current_lang = Locale.get_active()

        # Get last 3 webinars
        latest_webinars = (
            WebinarsPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )

        # Get last 3 formations
        latest_formations = (
            FormationsPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )

        # Update template context
        context = super().get_context(request)
        context["latest_webinars"] = latest_webinars
        context["latest_formations"] = latest_formations

        return context

    class Meta:
        verbose_name = "Events Page"


class WebinarsIndexPage(MetadataPageMixin, Page):
    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
    ]

    subpage_types = ["home.WebinarsPage"]

    parent_page_type = [
        "home.HomePage",
    ]

    def get_children(self):
        qs = super().get_children()
        qs = qs.order_by("-first_published_at")
        return qs

    class Meta:
        verbose_name = "Webinar Index Page"


class WebinarsPage(MetadataPageMixin, Page):
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
    )
    summary = models.TextField(blank=False)
    date = models.DateField("Webinar date")
    time = models.CharField(max_length=50, blank=False, null=True)
    location = models.CharField(max_length=100, blank=False, null=True)
    register_link = models.URLField(blank=True)
    replay_link = models.URLField(blank=True)

    overview = RichTextField(features=["h2", "h3", "h4", "ol", "ul", "bold", "italic", "link"], blank=True)

    agenda = StreamField([("agenda_layout", AgendaLayout())], blank=True, use_json_field=True)
    speakers = StreamField(
        [
            ("speaker_layout", SpeakerLayout()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("main_image"),
                FieldPanel("date"),
                FieldPanel("summary"),
                FieldPanel("time"),
                FieldPanel("location"),
                FieldPanel("register_link"),
                FieldPanel("replay_link"),
            ],
            heading="About Webinar",
        ),
        FieldPanel("overview"),
        FieldPanel("agenda"),
        FieldPanel("speakers"),
    ]

    parent_page_type = [
        "home.WebinarsIndexPage",
    ]

    def __str__(self):
        return self.title

    def get_month_published(self):
        month = self.date.strftime("%B")
        return month[:3]


class FormationsIndexPage(MetadataPageMixin, Page):
    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
    ]

    subpage_types = ["home.FormationsPage"]

    parent_page_type = [
        "home.HomePage",
    ]

    def get_children(self):
        qs = super().get_children()
        qs = qs.order_by("-first_published_at")
        return qs

    class Meta:
        verbose_name = "Formation Index Page"


class FormationsPage(MetadataPageMixin, Page):
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
    )
    summary = models.TextField(blank=False)
    starting_date = models.DateField("Starting date", null=True, blank=True)
    ending_date = models.DateField("Ending date", null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    register_link = models.CharField(blank=True)

    overview = RichTextField(blank=True)

    agenda = StreamField(
        [
            ("agenda_layout", AgendaLayout()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("main_image"),
                FieldPanel("starting_date"),
                FieldPanel("ending_date"),
                FieldPanel("summary"),
                FieldPanel("location"),
                FieldPanel("register_link"),
            ],
            heading="About Formation",
        ),
        FieldPanel("overview"),
        FieldPanel("agenda"),
    ]

    parent_page_type = [
        "home.FormationsIndexPage",
    ]

    def __str__(self):
        return self.title

    def get_start_month_published(self):
        return self.starting_date.strftime("%B")

    def get_end_month_published(self):
        return self.ending_date.strftime("%B")

    def get_split_start_month(self):
        month = self.starting_date.strftime("%B")
        return month[:3]

    def get_split_end_month(self):
        month = self.ending_date.strftime("%B")
        return month[:3]


class BlogIndexPage(MetadataPageMixin, Page):
    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
    ]

    subpage_types = ["home.BlogPage"]

    parent_page_type = [
        "home.HomePage",
    ]

    def get_context(self, request):
        # Get current language
        current_lang = Locale.get_active()

        # Get categories
        categories = BlogCategory.objects.filter(language=current_lang).all()

        # Update template context
        context = super().get_context(request)
        context["categories"] = categories
        return context

    def get_children(self):
        qs = super().get_children()
        qs = qs.order_by("-first_published_at")
        return qs

    class Meta:
        verbose_name = "Blog Index Page"


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey("BlogPage", related_name="tagged_items", on_delete=models.CASCADE)


class BlogTagIndexPage(Page):
    def get_context(self, request):
        # Get current language
        current_lang = Locale.get_active()
        # Filter by tag
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag, locale=current_lang).live().public()

        # Update template context
        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context


class BlogPage(MetadataPageMixin, Page):
    summary = models.TextField(blank=False)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
    )
    date = models.DateField("Post date")
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField("BlogCategory", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("tags"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Blog details",
        ),
        FieldPanel("summary"),
        FieldPanel("main_image"),
        FieldPanel("body"),
    ]

    parent_page_type = [
        "home.BlogIndexPage",
    ]

    def __str__(self):
        return self.title


class LangChoices(models.TextChoices):
    ENGLISH = ("English",)
    FRENCH = "French"


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    language = models.TextField(
        max_length=10,
        choices=LangChoices.choices,
        default=LangChoices.ENGLISH,
    )
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        null=True,
        max_length=255,
        help_text="A slug to identify posts by this category",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("language", widget=forms.Select),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "blog categories"
        ordering = ["name"]


class Mooc(models.Model):
    name = models.CharField(blank=False)
    url = models.SlugField(blank=False, unique=True)
    organisation = models.CharField(blank=False)
    course_image = models.ImageField(upload_to="moocs", blank=False, null=True)
    start_date = models.CharField(max_length=50, blank=False)
    start_display = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class NewsletterPage(MetadataPageMixin, Page):
    """NewsletterPage page model."""

    template = "pages/newsletter.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
            ],
            heading="Hero section",
        ),
    ]
    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    class Meta:
        verbose_name = "Newsletter Page"


class FlatMenuChoices(models.TextChoices):
    FOOTERMENU_1 = ("footer_menu_1",)
    FOOTERMENU_2 = "footer_menu_2"
    FOOTERMENU_3 = "footer_menu_3"


@register_setting
class GlobalSettings(TranslatableMixin, BaseGenericSetting):
    twitter_url = models.URLField(verbose_name="Twitter URL", blank=True, null=True)
    linkedin_url = models.URLField(verbose_name="Linkedin URL", blank=True, null=True)
    facebook_url = models.URLField(verbose_name="Facebook URL", blank=True, null=True)
    instagram_url = models.URLField(verbose_name="Instagram URL", blank=True, null=True)
    medium_url = models.URLField(verbose_name="Medium URL", blank=True, null=True)
    youtube_url = models.URLField(verbose_name="Youtube URL", blank=True, null=True)

    terms_and_conditions_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.SET_NULL
    )
    data_policy_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.SET_NULL
    )
    newsletter_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.SET_NULL
    )

    partners_section_heading = StreamField(
        [
            (
                "heading",
                blocks.StructBlock(
                    [
                        ("section_title_en", blocks.CharBlock(required=False, help_text=_("Add content in english"))),
                        ("section_title_fr", blocks.CharBlock(required=False, help_text=_("Add content in french"))),
                        (
                            "section_subtitle_en",
                            blocks.TextBlock(required=False, help_text=_("Add content in english")),
                        ),
                        (
                            "section_subtitle_fr",
                            blocks.TextBlock(required=False, help_text=_("Add content in french")),
                        ),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    main_partner = StreamField(
        [
            (
                "main_patner",
                blocks.StructBlock(
                    [
                        ("logo", ImageChooserBlock(required=False)),
                        ("organisation_url", blocks.URLBlock(required=False)),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    other_partners = StreamField(
        [
            (
                "partners",
                blocks.StructBlock(
                    [
                        (
                            "partner",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        ("logo", ImageChooserBlock(required=False)),
                                        ("organisation_url", blocks.URLBlock(required=False)),
                                    ],
                                ),
                            ),
                        )
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    newsletter_widget = StreamField(
        [
            (
                "newsletter_widget",
                blocks.StructBlock(
                    [
                        (
                            "newsletter_widget_title_en",
                            blocks.CharBlock(required=False, help_text=_("Add content in english")),
                        ),
                        (
                            "newsletter_widget_title_fr",
                            blocks.CharBlock(required=False, help_text=_("Add content in french")),
                        ),
                        (
                            "newsletter_widget_subtitle_en",
                            blocks.TextBlock(required=False, help_text=_("Add content in english")),
                        ),
                        (
                            "newsletter_widget_subtitle_fr",
                            blocks.TextBlock(required=False, help_text=_("Add content in french")),
                        ),
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    menus_widget = StreamField(
        [
            (
                "widgets",
                blocks.StructBlock(
                    [
                        (
                            "menu_widget",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "widget_title_en",
                                            blocks.CharBlock(required=False, help_text=_("Add content in english")),
                                        ),
                                        (
                                            "widget_title_fr",
                                            blocks.CharBlock(required=False, help_text=_("Add content in french")),
                                        ),
                                        (
                                            "flat_menu",
                                            blocks.ChoiceBlock(required=False, choices=FlatMenuChoices.choices),
                                        ),
                                    ],
                                ),
                            ),
                        )
                    ]
                ),
            ),
        ],
        min_num=0,
        max_num=1,
        blank=True,
        use_json_field=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("twitter_url"),
                FieldPanel("linkedin_url"),
                FieldPanel("facebook_url"),
                FieldPanel("instagram_url"),
                FieldPanel("medium_url"),
                FieldPanel("youtube_url"),
            ],
            "Social media settings",
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("terms_and_conditions_page"),
                PageChooserPanel("data_policy_page"),
                PageChooserPanel("newsletter_page"),
            ],
            "Utility pages",
        ),
        MultiFieldPanel(
            [
                FieldPanel("partners_section_heading"),
                FieldPanel("main_partner"),
                FieldPanel("other_partners"),
            ],
            "Partners Section",
        ),
        MultiFieldPanel(
            [FieldPanel("newsletter_widget"), FieldPanel("menus_widget")],
            "Footer Settings",
        ),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Global Settings"
