import time
from datetime import datetime
from xmlrpc.client import ServerProxy

from african_cities_lab.home import extra_settings
from african_cities_lab.home.tasks import openedx as openedx_tasks
from config import celery_app

# odoo settings/utils
odoo_base_url = extra_settings.ODOO_BASE_URL  # "https://epfl-exaf.odoo.com"
db = extra_settings.ODOO_DB
username = extra_settings.ODOO_USERNAME
password = extra_settings.ODOO_PASSWORD

common = ServerProxy(f"{odoo_base_url}/xmlrpc/2/common")
version = common.version()
uid = common.authenticate(db, username, password, {})

models = ServerProxy(f"{odoo_base_url}/xmlrpc/2/object")
models.execute_kw(db, uid, password, "res.partner", "check_access_rights", ["read"], {"raise_exception": False})


def find_contact_id(email):
    search_domain = [("email", "=", email)]
    contact_ids = models.execute_kw(db, uid, password, "res.partner", "search", [search_domain])
    return contact_ids[0] if contact_ids else None


def extract_country_id(country_code):
    if country_code:
        country_ids = models.execute_kw(db, uid, password, "res.country", "search", [[("code", "=", country_code)]])
        return country_ids[0] if country_ids else None
    else:
        return None


def get_date(date_str, default="2000-01-01"):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except TypeError:
        return default

    return dt.strftime("%Y-%m-%d")


@celery_app.task()
def update_odoo_contacts():
    accounts = openedx_tasks.get_accounts()
    for account in accounts:
        country_code = account.get("country", None)

        if country_code is not None:
            country_id = extract_country_id(country_code)
            if not country_id:
                print(f"Country {country_code} not found.")

        else:
            print("Country is missing in the row.")

        email = account["email"]
        contact_id = find_contact_id(email)
        base_data = {
            "x_studio_username": account["username"],
            "x_studio_last_login": get_date(account["last_login"]),
            "x_studio_date_joined_1": get_date(account["date_joined"]),
        }
        if contact_id:
            # Update the existing contact

            models.execute_kw(db, uid, password, "res.partner", "write", [[contact_id], base_data])
            print(f"Contact with email {email} updated.")
            time.sleep(0.5)
        else:
            # Create a new contact
            contact_data = {
                "name": account["name"],
                "email": email,
                "country_id": country_id,
                **base_data,
            }
            new_contact_id = models.execute_kw(db, uid, password, "res.partner", "create", [contact_data])
            print(f"Contact with email {email} created (id: {new_contact_id}).")
            time.sleep(0.5)
