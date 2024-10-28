from django.contrib import admin

from african_cities_lab.home.models import Mooc, Organization


@admin.register(Mooc)
class MoocAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass
