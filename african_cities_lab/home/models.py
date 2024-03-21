from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Locale, Orderable, Page
from wagtailmetadata.models import MetadataPageMixin

from african_cities_lab.home.layouts import AgendaLayout, SpeakerLayout


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
    banner_cta = models.URLField(blank=False)

    panels = [
        FieldPanel("carousel_image"),
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_cta"),
    ]


class HomePage(MetadataPageMixin, Page):
    """HomePage page model."""

    template = "pages/home.html"

    subpage_types = [
        "home.AboutPage",
        "home.MoocIndexPage",
        "home.WebinarsIndexPage",
        "home.FormationsIndexPage",
        "home.ContestPage",
        "home.ContactPage",
        "home.FlatPage",
    ]

    parent_page_type = [
        "wagtailcore.Page",
    ]
    max_count = 1

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=3, min_num=1, label="Caroussel Images")],
            heading="Slider",
        ),
    ]

    def get_context(self, request):
        # Get current language
        current_lang = Locale.get_active()

        # Get last 3 webinars
        latest_webinars = (
            WebinarsPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )
        # Update template context
        context = super().get_context(request)
        context["latest_webinars"] = latest_webinars

        return context

    class Meta:
        verbose_name = "Home Page"


class AboutPage(MetadataPageMixin, Page):
    """AboutPage page model."""

    template = "pages/about.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
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
        verbose_name = "About Page"


class ContestPage(MetadataPageMixin, Page):
    """ContestPage page model."""

    template = "pages/contest.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
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
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
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
        verbose_name = "Contact Page"


class TeamPage(MetadataPageMixin, Page):
    """TeamPage page model."""

    template = "pages/team.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
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
        verbose_name = "Team Page"


class FlatPage(MetadataPageMixin, Page):
    """FlatPage page model."""

    template = "pages/flat_page.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = RichTextField(features=["h2", "h3", "h4", "ol", "ul", "bold", "italic", "link"], blank=True)

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


class WebinarsIndexPage(MetadataPageMixin, Page):
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
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
    max_count = 1

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
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
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
    max_count = 1

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
    register_link = models.URLField(blank=True)

    overview = RichTextField(features=["h2", "h3", "h4", "ol", "ul", "bold", "italic", "link"], blank=True)

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
