import json

from edx_rest_api_client.client import OAuthAPIClient
from extra_settings.models import Setting

from african_cities_lab.home.models import Mooc, Organization
from config import celery_app

PAGE_SIZE = 100

EDX_BASE_URL = Setting.get("EDX_BASE_URL", default="https://courses.africancitieslab.org")
CLIENT_ID = Setting.get("EDX_CLIENT_ID", default="")
CLIENT_SECRET = Setting.get("EDX_CLIENT_SECRET", default="")
EDX_API_KEY = Setting.get("EDX_API_KEY", default="")

users_url = f"{EDX_BASE_URL}/api/user/v1/users"
accounts_url = f"{EDX_BASE_URL}/api/user/v1/accounts"
enrollments_url = f"{EDX_BASE_URL}/api/enrollment/v1/enrollments"
organizations_url = f"{EDX_BASE_URL}/api/organizations/v0/organizations"
courses_url = f"{EDX_BASE_URL}/api/courses/v1/courses/"
course_modes_base_url = f"{EDX_BASE_URL}/api/course_modes/v1/courses"
gradebook_base_url = f"{EDX_BASE_URL}/api/grades/v1/gradebook"
certificates_base_url = f"{EDX_BASE_URL}/api/certificates/v0/certificates"

client = OAuthAPIClient(EDX_BASE_URL, CLIENT_ID, CLIENT_SECRET)

get_kwargs = dict(
    headers={"X-EDX-API-KEY": EDX_API_KEY},
    params={"page_size": PAGE_SIZE},
)


@celery_app.task()
def get_organizations():
    organizations_resp = client.get(organizations_url).json()
    organizations = organizations_resp["results"]
    while "next" in organizations_resp and organizations_resp["next"] is not None:
        organizations_resp = client.get(organizations_resp["next"]).json()
        organizations.extend(organizations_resp["results"])
    return organizations


@celery_app.task()
def get_courses():
    courses_resp = client.get(courses_url).json()
    courses = courses_resp["results"]
    while "pagination" in courses_resp and courses_resp["pagination"]["next"] is not None:
        courses_resp = client.get(courses_resp["pagination"]["next"]).json()
        courses.extend(courses_resp["results"])
    return courses


@celery_app.task()
def update_courses():
    courses = get_courses()
    updated_courses = []
    created_courses = []
    created_organizations = []
    for course in courses:
        try:
            mooc = Mooc.objects.get(course_id=course["course_id"])
            # update the mooc object if any of the fields have changed
            if (
                mooc.name != course["name"]
                or mooc.start_date != course["start"]
                or mooc.image_url != course["media"]["image"]["raw"]
            ):
                mooc.name = course["name"]
                # we need to convert the start date string to YYYY-MM-DD format
                start_date = course["start"].split("T")[0]
                mooc.start_date = start_date
                mooc.image_url = course["media"]["image"]["raw"]
                mooc.save()
                updated_courses.append(course["course_id"])
        except Mooc.DoesNotExist:
            # create new mooc object
            # first see if the organization exists
            try:
                organization = Organization.objects.get(short_name=course["org"])
            except Organization.DoesNotExist:
                # the organization does not exist, create it
                # first get the organizations
                organizations = get_organizations()
                for _organization in organizations:
                    short_name = _organization["short_name"]
                    if short_name == course["org"]:
                        # get the logo url
                        client.get(f"{organizations_url}/{short_name}")
                        # if no logo, we need to use an empty string rather than None
                        logo_url = _organization["logo"]
                        if logo_url is None:
                            logo_url = ""
                        organization = Organization.objects.create(
                            name=_organization["name"],
                            short_name=_organization["short_name"],
                            logo_url=logo_url,
                        )
                        created_organizations.append(course["org"])
                        # no need to look for further organizations
                        break

            # now create the mooc object
            # we need to convert the start date string to YYYY-MM-DD format
            # TODO: DRY
            start_date = course["start"].split("T")[0]
            Mooc.objects.create(
                name=course["name"],
                course_id=course["course_id"],
                organization=organization,
                image_url=course["media"]["image"]["raw"],
                start_date=start_date,
            )
            created_courses.append(course["course_id"])

    return {
        "updated_courses": updated_courses,
        "created_courses": created_courses,
        "created_organizations": created_organizations,
    }


@celery_app.task()
def get_accounts():
    users_resp = client.get(users_url, **get_kwargs).json()

    usernames = [user["username"] for user in users_resp["results"]]
    accounts_resp = client.get(accounts_url, params={"username": ",".join(usernames)}).json()
    return accounts_resp


@celery_app.task()
def get_enrollment():
    enrollments_resp = client.get(enrollments_url).json()
    enrollments = enrollments_resp["results"]

    while enrollments_resp["next"] is not None:
        enrollments_resp = client.get(enrollments_resp["next"]).json()
        enrollments.extend(enrollments_resp["results"])

    return json.dumps(enrollments)


@celery_app.task
def get_certificates():
    certificates = []
    users_resp = client.get(users_url, **get_kwargs).json()
    accounts = get_accounts(users_resp)

    for account in accounts:
        username = account["username"]
        certificates_url = f"{certificates_base_url}/{username}"
        account_certificates = client.get(certificates_url).json()
        if account_certificates:
            certificates.extend(account_certificates)

    return json.dumps(certificates)


# users_resp = client.get(users_url, **get_kwargs).json()
# accounts = get_accounts(users_resp)
# while "next" in users_resp and users_resp["next"] is not None:
#     print(users_resp["next"])
#     users_resp = client.get(users_resp["next"], **get_kwargs).json()
#     accounts.extend(get_accounts(users_resp))

# enrollments_resp = client.get(enrollments_url).json()
# enrollments = enrollments_resp["results"]
# while enrollments_resp["next"] is not None:
#     print(enrollments_resp["next"])
#     enrollments_resp = client.get(enrollments_resp["next"]).json()
#     enrollments.extend(enrollments_resp["results"])

# courses_resp = client.get(courses_url).json()
# courses = courses_resp["results"]
# while "next" in courses_resp and courses_resp["next"] is not None:
#     print(courses_resp["next"])
#     courses_resp = client.get(courses_resp["next"]).json()
#     courses.extend(courses_resp["results"])


# # def is_honor(course_id):
# #     url = f"{course_modes_base_url}/{course_id}"
# #     for course_mode in client.get(url).json():
# #         if course_mode["mode_slug"] == "honor":
# #             return True
# #     return False


# # for course in courses:
# #     course_id = courses["course_id"]
# #     if is_honor(course_id):
# #         gradebook_url = f"{gradebook_base_url}/{course_id}"
# def get_certificates(account):
#     username = account["username"]
#     certificates_url = f"{certificates_base_url}/{username}"
#     return client.get(certificates_url).json()


# certificates = []
# num_accounts = len(accounts)
# for i, account in enumerate(accounts):
#     print(f"{i}/{num_accounts}")
#     account_certificates = get_certificates(account)
#     if account_certificates:
#         certificates.extend(
#             [(account, certificate) for certificate in account_certificates]
#         )

# # lower_limit = datetime.now(pytz.utc) + timedelta(days=7)
# # new_certificates = []
# # for account in accounts:
# #     certificates = get_certificates(account)
# #     if certificates:
# #         for certificate in certificates:
# #             if (
# #                 datetime.fromisoformat(
# #                     certificate["modified_date"].replace("Z", "+00:00")
# #                 )
# #                 > lower_limit
# #             ):
# #                 new_certificates.append((account, certificate))

# for data, dst_filename in zip(
#     [accounts, enrollments, certificates], ["accounts", "enrollments", "certificates"]
# ):
#     with open(dst_filename, "w") as dst:
#         json.dump(data, dst)
