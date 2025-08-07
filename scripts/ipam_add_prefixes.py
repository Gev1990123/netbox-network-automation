import sys
import os

# Add parent path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import csv
from pathlib import Path
from netbox_utils.functions import get_site, get_ipam_role, get_ipam_prefix
from netbox_utils.config import netbox


def load_prefixes(csv_path):
    prefixes = []
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            prefixes.append({
                'prefix': row['prefix'].strip(),
                'status': row['status'].strip(),
                'site': row['site'].strip(),
                'role': row.get('role', '').strip(),
                'description': row['description'].strip()
            })
    return prefixes

# Resolve CSV path
base_dir = Path(__file__).resolve().parent.parent
csv_file_path = base_dir / "data" / "ipam_add_prefixes.csv"

prefixes_data = load_prefixes(csv_file_path)

for prefix_data in prefixes_data:
    site_obj = get_site(netbox, prefix_data['site'])
    if not site_obj:
        print(f"❌ No site with name {prefix_data['site']}")
        continue

    role_obj = get_ipam_role(netbox, prefix_data['role']) if prefix_data['role'] else None
    existing_prefix = get_ipam_prefix(netbox, prefix_data['prefix'])

    if existing_prefix:
        print(f"⚠️ Prefix {prefix_data['prefix']} already exists: {getattr(existing_prefix, 'display', '')}")
        continue

    payload = {
        "prefix": prefix_data['prefix'],
        "status": prefix_data['status'],
        "site": site_obj.id,
        "description": prefix_data['description'],
        "scope_type": "dcim.site",
        "scope_id": site_obj.id
    }

    if role_obj:
        payload["role"] = role_obj.id
    elif prefix_data['role']:
        print(f"⚠️ Role '{prefix_data['role']}' not found. Creating without a role.")

    try:
        created = netbox.ipam.prefixes.create(payload)
        print(f"✅ Created Prefix: {prefix_data['prefix']}, {getattr(created, 'display', '')}")
    except Exception as e:
        print(f"❌ Failed to create prefix {prefix_data['prefix']}: {e}")