import json
import os
from datetime import datetime, timedelta
from django.conf import settings
import pytz
from edx_rest_api_client.client import OAuthAPIClient
from config import celery_app

PAGE_SIZE = 100
base_url = "https://courses.africancitieslab.org"
users_url = f"{base_url}/api/user/v1/users"
accounts_url = f"{base_url}/api/user/v1/accounts"
enrollments_url = f"{base_url}/api/enrollment/v1/enrollments"
courses_url = f"{base_url}/api/courses/v1/courses/"
course_modes_base_url = f"{base_url}/api/course_modes/v1/courses"
gradebook_base_url = f"{base_url}/api/grades/v1/gradebook"
certificates_base_url = f"{base_url}/api/certificates/v0/certificates"

client_id = settings.EDX_CLIENT_ID
client_secret = settings.EDX_CLIENT_SECRET
edx_api_key = settings.EDX_API_KEY

client = OAuthAPIClient(base_url, client_id, client_secret)

get_kwargs = dict(
    headers={"X-EDX-API-KEY": edx_api_key},
    params={"page_size": PAGE_SIZE},
)
@celery_app.task()
def get_accounts():
    users_resp = client.get(users_url, **get_kwargs).json()

    usernames = [user["username"] for user in users_resp["results"]]
    accounts_resp = client.get(
        accounts_url, params={"username": ",".join(usernames)}
    ).json()
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
            certificates.extend([(account, certificate) for certificate in account_certificates])
    
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
