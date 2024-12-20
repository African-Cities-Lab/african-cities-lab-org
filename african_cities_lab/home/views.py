import json

from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


def subscribe(email, list_id, merge_fields=None):
    """
    Contains code handling the communication to the mailchimp api
    to create a contact/member in an audience/list.
    """
    from african_cities_lab.home import extra_settings

    mailchimp = Client()
    mailchimp.set_config(
        {
            "api_key": extra_settings.MAILCHIMP_API_KEY,
            "server": extra_settings.MAILCHIMP_DATA_CENTER,
        }
    )

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    if merge_fields is not None:
        member_info["merge_fields"] = merge_fields

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print(f"API call successful: {response}")
        return response["status"]
    except ApiClientError as error:
        print(f"An exception occurred: {error.text}")
        if json.loads(error.text)["title"] == "Member Exists":
            return "exists"


def subscribe_event(request):
    if request.method == "POST":
        from african_cities_lab.home import extra_settings

        email = request.POST["EMAIL"]
        merge_fields = {
            "LNAME": request.POST["LNAME"],
            "FNAME": request.POST["FNAME"],
            "INSTITUT": request.POST["INSTITUT"],
            "FUNCTION": request.POST["FUNCTION"],
            "TITLE": request.POST["TITLE"],
            "COUNTRY": request.POST["COUNTRY"],
            "LINKEDIN": request.POST["LINKEDIN"],
        }

        if request.POST["site_language"] == "en":
            list_id = extra_settings.MAILCHIMP_WEBINAR_EN_LIST_ID
        else:  # "fr"
            list_id = extra_settings.MAILCHIMP_WEBINAR_FR_LIST_ID

        status = subscribe(email, list_id, merge_fields)
        if status == "subscribed":
            messages.success(
                request,
                _(
                    "Thank you for registering! A confirmation email has been sent to you, please check your mailbox or your spam."
                ),
            )  # message
        elif status == "exists":
            messages.info(
                request,
                _("Your email is already registered, please check your mailbox or your spam. Thank you!"),
            )  # message

    return render(
        request,
        "pages/event_subscribe_form.html",
        context={"title": _("Subscribe to the event")},
    )
