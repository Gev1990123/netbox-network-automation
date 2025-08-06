import sys
import os

# Ensure we can import from the parent directory (the project root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.config import netbox
from netbox_utils.functions import get_region


# List of region names to add
region_names = [
    "England",
    "East Midlands",
    "East of England",
    "London",
    "North East",
    "North West",
    "South East",
    "South West",
    "West Midlands",
    "Yorkshire and the Humber",
    "Northern Ireland",
    "Antrim",
    "Armagh",
    "Down",
    "Fermanagh",
    "Londonderry",
    "Tyrone",
    "Scotland",
    "Central Belt",
    "Highlands and Islands",
    "Southern Uplands",
    "Wales",
    "Mid Wales",
    "North Wales",
    "South Wales"
]

# Create each region
for name in region_names:
    slug = name.lower().replace(" ", "-")
    existing = get_region(netbox, name)

    if existing:
        print(f"Region '{name}' already exists, skipping.")
    else:
        region = netbox.dcim.regions.create({
        "name": name,
        "slug": slug
        })
        print(f"Created region: {region.name}")
