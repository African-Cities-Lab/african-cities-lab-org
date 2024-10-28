from extra_settings.models import Setting

EDX_BASE_URL = Setting.get("EDX_BASE_URL", default="https://courses.africancitieslab.org")
CLIENT_ID = Setting.get("EDX_CLIENT_ID", default="")
CLIENT_SECRET = Setting.get("EDX_CLIENT_SECRET", default="")
EDX_API_KEY = Setting.get("EDX_API_KEY", default="")

MAILCHIMP_API_KEY = Setting.get("MAILCHIMP_API_KEY", default="")
MAILCHIMP_DATA_CENTER = Setting.get("MAILCHIMP_DATA_CENTER", default="")
MAILCHIMP_WEBINAR_EN_LIST_ID = Setting.get("MAILCHIMP_WEBINAR_EN_LIST_ID", default="")
MAILCHIMP_WEBINAR_FR_LIST_ID = Setting.get("MAILCHIMP_WEBINAR_FR_LIST_ID", default="")
MAILCHIMP_NEWSLETTER_EN_ID = Setting.get("MAILCHIMP_NEWSLETTER_EN_ID", default="")
MAILCHIMP_NEWSLETTER_FR_ID = Setting.get("MAILCHIMP_NEWSLETTER_FR_ID", default="")
