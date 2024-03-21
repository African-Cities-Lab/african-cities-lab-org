from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # Language Redirect
    path("i18n/", include("django.conf.urls.i18n")),
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),
    # path(
    #     "webinars/",
    #     TemplateView.as_view(template_name="webinars/webinars_index_page.html"),
    #     name="webinars",
    # ),
    # path(
    #     "formations/",
    #     TemplateView.as_view(template_name="formations/formations_index_page.html"),
    #     name="formations",
    # ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Wagtail Admin
    path(settings.WAGTAIL_ADMIN_URL, include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # re_path(r"^search/$", search_views.search, name="search"),
    # User management
    path("users/", include("african_cities_lab.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    # For anything not caught by a more specific rule above, hand over to Wagtail's page
    # serving mechanism. This should be the last pattern in the list:
    # path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath of your site,
    # rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + i18n_patterns(
    # path("", include("home.urls")),
    path("", include(wagtail_urls)),
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
