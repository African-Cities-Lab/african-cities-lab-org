from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib import messages
from django.db import models
from django.shortcuts import render
from django.utils import timezone
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

from african_cities_lab.home import views
from african_cities_lab.home.blocks import (
    AgendaBlock,
    FeaturedPostsBlock,
    FormationsBlock,
    HeroBlock,
    NewsletterFormBlock,
    SectionBlock,
    SectionPictureBlock,
    SpeakersBlock,
    WebinarsBlock,
)

HERO_BLOCKS = [
    ("hero_block", HeroBlock()),
]

BODY_BLOCKS = [
    ("section_picture_block", SectionPictureBlock()),
    ("section_block", SectionBlock()),
]

PAGE_BLOCKS = HERO_BLOCKS + BODY_BLOCKS

HOME_BLOCKS = BODY_BLOCKS + [
    ("featured_posts_block", FeaturedPostsBlock()),
]

EVENTS_BLOCKS = PAGE_BLOCKS + [
    ("featured_posts_block", FeaturedPostsBlock()),
]


class Organization(models.Model):
    """Organization model."""

    name = models.CharField()
    short_name = models.CharField(max_length=50, blank=True)
    logo_url = models.URLField()

    def __str__(self):
        return self.name


class Mooc(models.Model):
    """Mooc model."""

    name = models.CharField()
    url = models.URLField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    image_url = models.URLField()
    start_date = models.DateField()

    def __str__(self):
        return self.name

    def is_new(self):
        # whether the mooc's start date is within the last 90 days
        return self.start_date >= timezone.now().date() - timedelta(days=90)


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
    banner_cta = models.URLField(blank=False, help_text=_("Enter button URL here"))
    banner_button_label = models.CharField(blank=False, default=_("Enter button label here (e.g., Learn more)"))

    panels = [
        FieldPanel("carousel_image"),
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_cta"),
        FieldPanel("banner_button_label"),
    ]


class HomePage(MetadataPageMixin, Page):
    """HomePage model."""

    body = StreamField(
        HOME_BLOCKS,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=3, min_num=1, label=_("Caroussel Images"))],
            heading=_("Slider"),
        ),
        FieldPanel("body"),
    ]

    subpage_types = [
        "home.EventIndexPage",
        "home.BlogIndexPage",
        "home.WebinarIndexPage",
        "home.FormationIndexPage",
        "home.FlatPage",
        "home.NewsletterPage",
    ]
    parent_page_type = [
        "wagtailcore.Page",
    ]
    max_count = 1

    def get_context(self, request):
        # Get current language
        current_lang = Locale.get_active()

        # Get last 3 webinars
        latest_webinars = (
            WebinarPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )
        # Get last 3 articles
        latest_articles = (
            BlogPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )

        # Get latest 6 moocs
        latest_moocs = Mooc.objects.order_by("-start_date")[:6]

        # Update template context
        context = super().get_context(request)
        context["webinars"] = latest_webinars
        context["articles"] = latest_articles
        context["moocs"] = latest_moocs

        return context

    class Meta:
        verbose_name = _("Home Page")


class FlatPage(MetadataPageMixin, Page):
    """FlatPage model."""

    body = StreamField(
        PAGE_BLOCKS,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_type = [
        "home.HomePage",
    ]

    class Meta:
        verbose_name = _("Flat Page")


class IndexPage(Page):
    """IndexPage model."""

    body = StreamField(
        PAGE_BLOCKS,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_children(self):
        qs = super().get_children()
        qs = qs.order_by("-first_published_at")
        return qs

    class Meta:
        abstract = True
        verbose_name = _("Index Page")


class EventIndexPage(MetadataPageMixin, IndexPage):
    """EventIndexPage model."""

    body = StreamField(
        EVENTS_BLOCKS,
        blank=True,
        use_json_field=True,
    )

    template = "home/flat_page.html"
    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    def get_context(self, request):
        # Get current language
        current_lang = Locale.get_active()

        # Get last 3 webinars
        latest_webinars = (
            WebinarPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )

        # Get last 3 formations
        latest_formations = (
            FormationPage.objects.filter(locale=current_lang).live().public().order_by("-first_published_at")[:3]
        )

        # Update template context
        context = super().get_context(request)
        context["webinars"] = latest_webinars
        context["formations"] = latest_formations

        return context

    class Meta:
        verbose_name = _("Event Index Page")


class WebinarIndexPage(MetadataPageMixin, IndexPage):
    """WebinarIndexPage model."""

    body = StreamField(
        PAGE_BLOCKS + [("webinars", WebinarsBlock())],
        block_counts={"webinars": {"min_num": 1, "max_num": 1}},
        blank=True,
        use_json_field=True,
    )

    template = "home/flat_page.html"
    subpage_types = ["home.WebinarPage"]
    parent_page_type = [
        "home.HomePage",
    ]

    class Meta:
        verbose_name = _("Webinar Index Page")


class WebinarPage(MetadataPageMixin, Page):
    """WebinarPage model."""

    main_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
    )
    summary = models.TextField(blank=False)
    date = models.DateField()
    time = models.CharField(max_length=50, blank=False, null=True)
    location = models.CharField(max_length=100, blank=False, null=True)
    register_link = models.URLField(blank=True)
    replay_link = models.URLField(blank=True)
    overview = RichTextField(features=["h2", "h3", "h4", "ol", "ul", "bold", "italic", "link"], blank=True)
    agenda = StreamField([("agenda", AgendaBlock())], blank=True, use_json_field=True)
    speakers = StreamField(
        [
            ("speakers", SpeakersBlock()),
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
            heading=_("About Webinar"),
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


class FormationIndexPage(MetadataPageMixin, IndexPage):
    """FormationIndexPage model."""

    body = StreamField(
        PAGE_BLOCKS + [("formations", FormationsBlock())],
        block_counts={"formations": {"min_num": 1, "max_num": 1}},
        blank=True,
        use_json_field=True,
    )

    template = "home/flat_page.html"
    subpage_types = ["home.FormationPage"]
    parent_page_type = [
        "home.HomePage",
    ]

    class Meta:
        verbose_name = _("Formation Index Page")


class FormationPage(MetadataPageMixin, Page):
    """FormationPage model."""

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
            ("agenda", AgendaBlock()),
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
            heading=_("About Formation"),
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


class BlogIndexPage(MetadataPageMixin, IndexPage):
    """BlogIndexPage model."""

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

    class Meta:
        verbose_name = _("Blog Index Page")


class BlogPageTag(TaggedItemBase):
    """BlogPageTag model."""

    content_object = ParentalKey("BlogPage", related_name="tagged_items", on_delete=models.CASCADE)


class BlogTagIndexPage(Page):
    """BlogTagIndexPage model."""

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
    """BlogPage model."""

    summary = models.TextField(blank=False)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
    )
    date = models.DateField()
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
            heading=_("Blog details"),
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
    """BlogCategory model."""

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
        help_text=_("A slug to identify posts by this category"),
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("language", widget=forms.Select),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ["name"]


class NewsletterPage(MetadataPageMixin, Page):
    """NewsletterPage model."""

    body = StreamField(
        PAGE_BLOCKS + [("newsletter_form", NewsletterFormBlock())],
        block_counts={"newsletter_form": {"min_num": 1, "max_num": 1}},
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_type = [
        "home.HomePage",
    ]
    max_count = 1

    def serve(self, request):
        if request.method == "POST":
            email = request.POST["EMAIL"]
            merge_fields = {
                "LNAME": request.POST["LNAME"],
                "FNAME": request.POST["FNAME"],
            }

            if request.POST["site_language"] == "en":
                list_id = settings.MAILCHIMP_NEWSLETTER_EN_ID
            else:  # "fr"
                list_id = settings.MAILCHIMP_NEWSLETTER_FR_ID

            status = views.subscribe(email, list_id, merge_fields)
            if status == "subscribed":
                messages.success(
                    request,
                    _(
                        "Thank you for subscribing to our newsletter. Watch your mailbox for news, updates and courses from the African Cities Lab very soon!"
                    ),
                )  # message
            elif status == "exists":
                messages.info(
                    request,
                    _(
                        "Your email is already registered. Watch your mailbox for news, updates and courses from the African Cities Lab very soon!"
                    ),
                )  # message

        return render(request, "home/newsletter_page.html", {"page": self})

    class Meta:
        verbose_name = _("Newsletter Page")


class FlatMenuChoices(models.TextChoices):
    """FlatMenuChoices model."""

    FOOTERMENU_1 = ("footer_menu_1",)
    FOOTERMENU_2 = "footer_menu_2"
    FOOTERMENU_3 = "footer_menu_3"


@register_setting
class GlobalSettings(TranslatableMixin, BaseGenericSetting):
    """GlobalSettings."""

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
            _("Social media settings"),
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("terms_and_conditions_page"),
                PageChooserPanel("data_policy_page"),
                PageChooserPanel("newsletter_page"),
            ],
            _("Utility pages"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("partners_section_heading"),
                FieldPanel("main_partner"),
                FieldPanel("other_partners"),
            ],
            _("Partners Section"),
        ),
        MultiFieldPanel(
            [FieldPanel("newsletter_widget"), FieldPanel("menus_widget")],
            _("Footer Settings"),
        ),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = _("Global Settings")
