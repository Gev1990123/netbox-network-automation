import os
import requests
import pynetbox
from dotenv import load_dotenv
import urllib3

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NETBOX_URL = os.getenv("NETBOX_URL")
NETBOX_TOKEN = os.getenv("NETBOX_API_TOKEN")
VEFIRY_SSL = os.getenv("NETBOX_VERIFY_SSL", "false").strip().lower() in ("1", "true", "yes")

session = requests.Session()
session.verify = VEFIRY_SSL

if not NETBOX_URL or not NETBOX_TOKEN:
    raise EnvironmentError("Missing NETBOX_URL or NETBOX_API_TOKEN in environment variables.")

netbox = pynetbox.api(NETBOX_URL, token=NETBOX_TOKEN)
netbox.http_session = session
