import sys
import os

# Ensure we can import from the parent directory (the project root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from netbox_utils.functions import get_region, get_site
from netbox_utils.config import netbox

# List of sites to add
sites = [
    {'site_name': 'Belfast','region': 'Antrim'},
    {'site_name': 'Birmingham', 'region': 'West Midlands'},
    {'site_name': 'Cardiff', 'region': 'South Wales'},
    {'site_name': 'Exeter', 'region': 'South West'},
    {'site_name': 'Glasgow', 'region': 'Central Belt'},
    {'site_name': 'Leeds', 'region': 'Yorkshire and the Humber'},
    {'site_name': 'London', 'region': 'London'},
    {'site_name': 'Newcastle', 'region': 'North East'},
    {'site_name': 'Newtown', 'region': 'Mid Wales'},
]


# Create each site
for site in sites:
    site_name = site['site_name']
    region_name = site['region']

    
    # Get the region object by name
    region = get_region(netbox, region_name)

    if region:
        site_present = get_site(netbox, site_name)

        if site_present:
            print(f'{site_name} is already created. ')
        else:
            # Create the site
            created_site = netbox.dcim.sites.create({
                "name": site_name,
                "slug": site_name.lower().replace(" ","-"),
                "region": region.id
            })

            print(f"Created Site: {site_name}")
    else:
        print(f"Region '{region_name}' not found. Site '{site_name}' not created.")